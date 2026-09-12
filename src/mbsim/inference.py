"""Phase A: prove the simulator can solve its own tau/amyloid inverse problem.

Forward direction (already fully built elsewhere in this package): given a
pathology profile theta = {"tau": intensity, "amyloid": intensity} (0-100
each, exactly `mbsim.perturbations.PERTURBATION_TYPES`'s existing scale),
`mbsim.trials.run_trials` + `mbsim.perturbations`/`mbsim.damage` already
produce a noisy distribution of simulated signal-delay outcomes.

This module adds the missing INVERSE direction the project's clinical plan
needs: given an observed 5s/10s/30s time-perception deviation profile (real
patient data, once it exists — see `data/clinical/README.md`), which
tau/amyloid profile is most consistent with it? Per the team's explicit
framing, this is deliberately NOT a point-estimate diagnosis ("this patient
has 55% amyloid") — it is a probabilistic hypothesis-consistency signal
against *this simulator's own modeling assumptions*, using Approximate
Bayesian Computation (ABC): simulate many candidate theta, keep the ones
whose simulated summary statistics land closest to the observed ones, and
report that accepted set as an (uncalibrated, until `run_sbc` below proves
otherwise) approximate posterior.

Before touching any real patient data, `run_sbc` (simulation-based
calibration) answers a narrower, fully synthetic question first: if we
already know the true theta because WE generated it, does this inference
procedure recover it? Only once that self-recovery test passes does it make
sense to point this machinery at real data — and even then, the result is a
hypothesis-generation tool, not a diagnostic; confirming actual amyloid/tau
levels requires independent CSF/PET biomarker validation.

Three modeling facts worth knowing before using any of this:

1. **Tau and amyloid must be made distinguishable, or this is unsolvable by
   construction.** In `mbsim.perturbations`, both default to the exact same
   channel, reduction function, and target scope (every edge) — two theta
   with equal combined severity `1-(1-tau/100)(1-amyloid/100)` produce
   *identical* simulated output, so no inference method could ever tell them
   apart. `theta_to_perturbations` below breaks this by giving amyloid a
   narrower default scope via the *already-existing* `target_neuropils`
   mechanism (`mbsim.targeting`'s own docstring anticipates exactly this use
   case: "compartment-specific plaque deposition"). This is a modeling
   assumption introduced here for Phase A, not a change to
   `mbsim.perturbations`'s general-purpose defaults (a UI user may still
   legitimately want brain-wide amyloid) — flag it to the medical team for
   literature backing, exactly as `damage.py`'s placeholder curves are
   flagged.
2. **GABA/APL are exact no-ops on the bundled fixture graph** (no GABA edges,
   no APL-labeled neuron in `data/fixtures/`), so `THETA_DIMS` is scoped to
   `("tau", "amyloid")` — validating the threshold channel needs the real
   connectome or a hand-extended fixture.
3. **The 5s/10s/30s "profile" is flat by construction today.**
   `mbsim.perception`'s delay_ratio does not depend on the interval length,
   so `simulate_patient_profile` deliberately reduces each synthetic
   patient's observation to two honest summary statistics — pooled mean
   %-deviation and pooled coefficient of variation (Weber fraction) — rather
   than a 6-number vector (3 means + 3 CVs) that would look like 6
   independent pieces of evidence when it is really the same 2 numbers
   repeated three times. `per_interval` is still returned, shaped like the
   clinical CSV, for transparency/plotting — just don't feed all 6 of its
   numbers into `abc_reject` as if independent.

Nothing here is wired into `app.py`/`cli.py` — it is an offline research
script, run the way `pytest` or a standalone analysis script is, not a live
UI feature (a "Hypothesis Consistency" tab is a separate, later addition
once Phase A passes).
"""

import statistics
from typing import Callable

import numpy as np
from scipy import stats as scipy_stats

from mbsim.calibration import ms_per_time_unit
from mbsim.damage import (
    SlowdownFn,
    ThresholdFn,
    damaged_conduction_velocity,
    damaged_threshold,
    linear_slowdown,
    linear_threshold_increase,
)
from mbsim.perturbations import per_edge_velocity_severity, per_node_threshold_severity
from mbsim.simulation import simulate
from mbsim.trials import DEFAULT_NOISE_STD, run_trials

THETA_DIMS = ("tau", "amyloid")
TARGET_INTERVALS_S = (5.0, 10.0, 30.0)

# The calyx compartment (PN->KC synapses) — a real Codex neuropil label, not a
# fixture-only artifact — used to give amyloid a narrower default scope than
# tau's brain-wide default (see point 1 in the module docstring). Swap for a
# literature-backed compartment list once the medical team specifies one.
AMYLOID_DEFAULT_NEUROPILS = ("MB_CA_L",)


def theta_to_perturbations(theta: dict[str, float]) -> list[dict]:
    """A pathology profile `{"tau": intensity, "amyloid": intensity}`
    (0-100 each) -> the `perturbations` list `mbsim.metrics.compare` /
    `mbsim.trials.compare_trials` already know how to consume."""
    perturbations = []
    tau = theta.get("tau", 0.0)
    if tau > 0:
        perturbations.append({"type": "tau", "intensity": tau})
    amyloid = theta.get("amyloid", 0.0)
    if amyloid > 0:
        perturbations.append(
            {"type": "amyloid", "intensity": amyloid, "target_neuropils": list(AMYLOID_DEFAULT_NEUROPILS)}
        )
    return perturbations


def combined_severity(theta: dict[str, float]) -> float:
    """The one quantity this forward model can actually identify today (see
    module docstring point 1): the independent-multiplicative-combination
    severity `mbsim.perturbations` would compute if tau and amyloid shared
    the same scope. Individual tau/amyloid recovery is expected to show a
    ridge along constant `combined_severity`, not a point — that is the
    honest correct answer given the forward model's structure, not a bug."""
    tau_frac = max(0.0, min(1.0, theta.get("tau", 0.0) / 100.0))
    amyloid_frac = max(0.0, min(1.0, theta.get("amyloid", 0.0) / 100.0))
    return 1.0 - (1.0 - tau_frac) * (1.0 - amyloid_frac)


def _damage_overrides(
    graph,
    perturbations: list[dict],
    base_conduction_velocity: float,
    threshold: float,
    slowdown_fn: SlowdownFn = linear_slowdown,
    threshold_fn: ThresholdFn = linear_threshold_increase,
) -> tuple[dict[tuple, float], dict[str, float]]:
    """The edge_velocity/node_threshold override dicts `run_trials` accepts,
    built from a perturbations list — exactly `mbsim.trials.compare_trials`'s
    existing damage-resolution preamble, factored out so
    `simulate_patient_profile` can call `run_trials` directly on only the
    damaged side (see module docstring / class docstring in `run_sbc`) rather
    than going through `compare_trials`, which always re-simulates a second,
    independently-noisy healthy side too."""
    edge_severity = per_edge_velocity_severity(graph, perturbations)
    node_severity = per_node_threshold_severity(graph, perturbations)
    edge_velocity = {
        edge: damaged_conduction_velocity(base_conduction_velocity, severity, slowdown_fn)
        for edge, severity in edge_severity.items()
    }
    node_threshold = {
        node: damaged_threshold(threshold, severity, threshold_fn) for node, severity in node_severity.items()
    }
    return edge_velocity, node_threshold


def _mean_reached(fire_times: dict[str, float], nodes: list[str]) -> float | None:
    reached = [fire_times[n] for n in nodes if n in fire_times]
    return statistics.mean(reached) if reached else None


def simulate_patient_profile(
    graph,
    input_nodes: list[str],
    output_nodes: list[str],
    theta: dict[str, float],
    base_conduction_velocity: float = 1.0,
    threshold: float = 1.0,
    target_intervals_s: tuple[float, ...] = TARGET_INTERVALS_S,
    n_trials: int = 10,
    noise_std: float = DEFAULT_NOISE_STD,
    seed: int | None = None,
) -> dict:
    """theta -> a synthetic-"patient" 5s/10s/30s deviation profile.

    The healthy arrival time is computed ONCE, deterministically (theta never
    touches the healthy structure, so there is nothing patient-specific to
    re-simulate on that side — this is exactly what `mbsim.metrics.compare`
    already does for `healthy_fire_times`). Only the damaged side is run
    through `n_trials` of `mbsim.trials.run_trials`'s Monte Carlo noise, and
    each trial's damaged/healthy ratio becomes one noisy "session" a
    synthetic patient could have produced.

    Raises `ValueError` if no output node is reached in the healthy run, or
    if no output node is reached in every one of the `n_trials` damaged
    runs (a theta severe enough to fully block the pathway sometimes/always —
    itself informative, but outside what this Phase A profile supports).
    """
    healthy_fire_times = simulate(graph, input_nodes, base_conduction_velocity, threshold)
    healthy_arrival = _mean_reached(healthy_fire_times, output_nodes)
    if healthy_arrival is None or healthy_arrival <= 0:
        raise ValueError("No output node reached in the healthy run — check graph/input_nodes/output_nodes.")
    healthy_ms = healthy_arrival * ms_per_time_unit()

    perturbations = theta_to_perturbations(theta)
    edge_velocity, node_threshold = _damage_overrides(graph, perturbations, base_conduction_velocity, threshold)
    samples, _ = run_trials(
        graph,
        input_nodes,
        output_nodes,
        base_conduction_velocity,
        threshold,
        edge_velocity=edge_velocity,
        node_threshold=node_threshold,
        n_trials=n_trials,
        noise_std=noise_std,
        seed=seed,
    )
    complete_nodes = [node for node in output_nodes if len(samples.get(node, [])) == n_trials]
    if not complete_nodes:
        raise ValueError(
            "No output node was reached in every damaged trial for this theta "
            f"({theta!r}) — likely too severe (near-100 velocity-channel intensity "
            "fully blocks the pathway); simulate_patient_profile only supports the "
            "fully-reached case for Phase A."
        )
    damaged_arrivals_per_trial = [
        statistics.mean(samples[node][i] for node in complete_nodes) for i in range(n_trials)
    ]
    delay_ratio_samples = [(arrival * ms_per_time_unit()) / healthy_ms for arrival in damaged_arrivals_per_trial]

    # (delay_ratio - 1) * 100 does not depend on target_interval_s (see module
    # docstring point 3) — the same delay_ratio samples are reused for every
    # interval rather than redrawn per interval, since redrawing would make a
    # single underlying signal look like three independent ones.
    pct_deviation_samples = [(ratio - 1.0) * 100.0 for ratio in delay_ratio_samples]
    mean_pct_deviation = statistics.mean(pct_deviation_samples)
    mean_ratio = statistics.mean(delay_ratio_samples)
    cv = (
        statistics.stdev(delay_ratio_samples) / mean_ratio
        if len(delay_ratio_samples) > 1 and mean_ratio != 0
        else None
    )
    per_interval = {interval_s: {"mean_pct_deviation": mean_pct_deviation, "cv": cv} for interval_s in target_intervals_s}

    return {
        "theta": dict(theta),
        "target_intervals_s": tuple(target_intervals_s),
        "healthy_ms": healthy_ms,
        "delay_ratio_samples": delay_ratio_samples,
        "pct_deviation_samples": pct_deviation_samples,
        "per_interval": per_interval,
    }


def summary_stats(profile: dict) -> np.ndarray:
    """Reduce a `simulate_patient_profile` (or real-patient-derived, once
    Phase B wires that up) profile to the two honest, non-redundant summary
    statistics ABC should compare on: pooled mean %-deviation and pooled
    Weber-fraction-like CV (see module docstring point 3 for why not six)."""
    first = next(iter(profile["per_interval"].values()))
    cv = first["cv"] if first["cv"] is not None else 0.0
    return np.array([first["mean_pct_deviation"], cv])


def default_prior_sampler(
    rng: np.random.Generator, tau_range: tuple[float, float] = (0.0, 80.0), amyloid_range: tuple[float, float] = (0.0, 80.0)
) -> dict[str, float]:
    """Uniform prior over each dimension, bounded away from 100 to avoid the
    fully-blocked-pathway case `simulate_patient_profile` doesn't support. A
    placeholder, in the same spirit as `damage.py`'s curves — replace with a
    literature-informed prior (e.g. a Beta skewed toward mild-to-moderate
    pathology) once the medical team supplies one."""
    return {"tau": float(rng.uniform(*tau_range)), "amyloid": float(rng.uniform(*amyloid_range))}


PriorSampler = Callable[[np.random.Generator], dict[str, float]]
ForwardFn = Callable[[dict[str, float], np.random.Generator], np.ndarray]


def abc_reject(
    observed_stats: np.ndarray,
    prior_sampler: PriorSampler,
    forward_fn: ForwardFn,
    n_sims: int = 20_000,
    accept_quantile: float = 0.01,
    seed: int | None = None,
) -> dict:
    """Rejection-ABC: draw `n_sims` theta from the prior, forward-simulate
    each to its summary stats, keep the closest `accept_quantile` fraction by
    standardized Euclidean distance (standardized by the prior-predictive
    spread, so no one statistic's raw units dominate) as the approximate
    posterior sample.
    """
    rng = np.random.default_rng(seed)
    thetas = [prior_sampler(rng) for _ in range(n_sims)]
    stats = np.array([forward_fn(theta, rng) for theta in thetas])
    scale = stats.std(axis=0)
    scale[scale == 0] = 1.0
    distances = np.linalg.norm((stats - observed_stats) / scale, axis=1)
    n_accept = max(1, int(round(n_sims * accept_quantile)))
    accepted_idx = np.argsort(distances)[:n_accept]
    return {
        "accepted_theta": [thetas[i] for i in accepted_idx],
        "accepted_stats": stats[accepted_idx],
        "n_sims": n_sims,
        "n_accepted": n_accept,
    }


def run_sbc(
    graph,
    input_nodes: list[str],
    output_nodes: list[str],
    prior_sampler: PriorSampler = default_prior_sampler,
    n_repetitions: int = 200,
    n_trials_observed: int = 10,
    n_sims_per_repetition: int = 2_000,
    n_trials_per_sim: int = 3,
    accept_quantile: float = 0.05,
    target_intervals_s: tuple[float, ...] = TARGET_INTERVALS_S,
    seed: int | None = None,
) -> dict:
    """The self-recovery falsification test (simulation-based calibration):
    for `n_repetitions` known theta drawn from the prior, synthesize a noisy
    "patient" observation, run ABC against it, and record where the true
    `combined_severity(theta)` ranks within the accepted posterior sample.

    Under correct calibration, `rank / n_accepted` across all repetitions
    should be uniformly distributed on [0, 1] — check with
    `sbc_rank_uniformity_pvalue`. A skewed distribution means the inference
    procedure is measurably miscalibrated (see module docstring); this must
    pass before pointing `abc_reject` at any real patient data.

    Runs entirely on synthetic data — no real patient data is used or
    required. Intended for the small bundled fixture graph, where each
    `simulate()` call is sub-millisecond; the default `n_sims_per_repetition`
    can be much cheaper (fewer `n_trials_per_sim`) than the observed
    synthetic patient's own trial count, since it's a cheap proposal
    distribution, not the noisy "observation" itself.
    """
    rng = np.random.default_rng(seed)
    ranks = []
    for _ in range(n_repetitions):
        theta_true = prior_sampler(rng)
        observed_profile = simulate_patient_profile(
            graph,
            input_nodes,
            output_nodes,
            theta_true,
            target_intervals_s=target_intervals_s,
            n_trials=n_trials_observed,
            seed=int(rng.integers(0, 2**31 - 1)),
        )
        observed_stats = summary_stats(observed_profile)

        def forward_fn(
            theta: dict[str, float],
            inner_rng: np.random.Generator,
            _graph=graph,
            _input_nodes=input_nodes,
            _output_nodes=output_nodes,
        ) -> np.ndarray:
            profile = simulate_patient_profile(
                _graph,
                _input_nodes,
                _output_nodes,
                theta,
                target_intervals_s=target_intervals_s,
                n_trials=n_trials_per_sim,
                seed=int(inner_rng.integers(0, 2**31 - 1)),
            )
            return summary_stats(profile)

        result = abc_reject(
            observed_stats,
            prior_sampler,
            forward_fn,
            n_sims=n_sims_per_repetition,
            accept_quantile=accept_quantile,
            seed=int(rng.integers(0, 2**31 - 1)),
        )
        accepted_c = np.array([combined_severity(theta) for theta in result["accepted_theta"]])
        true_c = combined_severity(theta_true)
        ranks.append({"rank": int((accepted_c < true_c).sum()), "n_accepted": len(accepted_c), "true_c": true_c})
    return {"ranks": ranks, "n_repetitions": n_repetitions}


def sbc_rank_uniformity_pvalue(ranks: list[dict]) -> float:
    """KS-test p-value for whether `run_sbc`'s rank statistics are consistent
    with the uniform distribution correct calibration predicts. A small
    p-value (conventionally < 0.05) means the *inference procedure* is
    measurably miscalibrated — not that any one patient's estimate is wrong."""
    normalized = [r["rank"] / r["n_accepted"] for r in ranks if r["n_accepted"] > 0]
    if len(normalized) < 2:
        raise ValueError("Need at least 2 repetitions with n_accepted > 0 to test uniformity.")
    _statistic, p_value = scipy_stats.kstest(normalized, "uniform")
    return float(p_value)
