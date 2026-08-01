"""Monte Carlo trial-to-trial variability -> an actual (not assumed) Weber fraction.

`mbsim.metrics.compare` reports one deterministic healthy run vs. one
deterministic damaged run — a single point estimate each. The Weber fraction
this project's pitch cites (~5-13% variability in healthy humans, per
Weber-Fechner psychophysics literature) is instead a property of a
*distribution* across repeated trials of the same network, not something a
single comparison can produce. This module adds the missing repetition:
each trial redraws independent noise on top of conduction velocity before
running `mbsim.simulation.simulate`, so a real empirical coefficient of
variation (CV = std/mean of arrival time across trials) — a direct
Weber-fraction-like quantity — can be computed from many runs instead of
assumed or left absent.

The noise model is a placeholder, in the same spirit as `damage.py`:
log-normal multiplicative jitter on conduction velocity (log-normal keeps
velocity positive regardless of noise magnitude), independently drawn per
trial and per edge. Swap `_jittered_velocity` for a literature/lab-derived
per-synapse or per-neuron noise model once available — nothing else in this
module needs to change.
"""

import random
import statistics

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

DEFAULT_N_TRIALS = 30
DEFAULT_NOISE_STD = 0.1


def _jittered_velocity(base_velocity: float, noise_std: float, rng: random.Random) -> float:
    if noise_std <= 0:
        return base_velocity
    return base_velocity * rng.lognormvariate(0.0, noise_std)


def run_trials(
    graph,
    input_nodes: list[str],
    output_nodes: list[str],
    base_conduction_velocity: float = 1.0,
    threshold: float = 1.0,
    edge_velocity: dict[tuple, float] | None = None,
    node_threshold: dict[str, float] | None = None,
    n_trials: int = DEFAULT_N_TRIALS,
    noise_std: float = DEFAULT_NOISE_STD,
    seed: int | None = None,
) -> tuple[dict[str, list[float]], dict[str, dict]]:
    """Run `n_trials` independent noisy simulations.

    `edge_velocity`/`node_threshold` are the same *damage* overrides
    `mbsim.metrics.compare` builds from targeted perturbations — pass
    None/{} for a healthy run. Noise is layered independently on top of them
    each trial, not a substitute for them.

    Returns `(samples, stats)`: `samples` is `{node: [arrival_time, ...]}` for
    every output node reached in at least one trial; `stats` is
    `{node: {"n", "mean", "std", "cv"}}`, where `cv` (coefficient of
    variation = std/mean) is the empirical Weber-fraction-like quantity —
    `None` if fewer than 2 trials reached that node.
    """
    rng = random.Random(seed)
    edge_velocity = edge_velocity or {}
    node_threshold = node_threshold or {}
    samples: dict[str, list[float]] = {node: [] for node in output_nodes}

    for _ in range(n_trials):
        trial_velocity = _jittered_velocity(base_conduction_velocity, noise_std, rng)
        trial_edge_velocity = {edge: _jittered_velocity(v, noise_std, rng) for edge, v in edge_velocity.items()}
        fire_times = simulate(
            graph,
            input_nodes,
            conduction_velocity=trial_velocity,
            threshold=threshold,
            edge_velocity=trial_edge_velocity,
            node_threshold=node_threshold,
        )
        for node in output_nodes:
            if node in fire_times:
                samples[node].append(fire_times[node])

    stats = {}
    for node, values in samples.items():
        if len(values) < 2:
            stats[node] = {"n": len(values), "mean": values[0] if values else None, "std": None, "cv": None}
            continue
        mean = statistics.mean(values)
        std = statistics.stdev(values)
        stats[node] = {"n": len(values), "mean": mean, "std": std, "cv": (std / mean) if mean else None}
    return samples, stats


def mean_weber_fraction(stats: dict[str, dict]) -> float | None:
    """Mean coefficient of variation across output nodes with enough trials
    to compute one — the aggregate empirical Weber-fraction-like estimate for
    a condition (healthy or damaged)."""
    cvs = [s["cv"] for s in stats.values() if s["cv"] is not None]
    return sum(cvs) / len(cvs) if cvs else None


def compare_trials(
    graph,
    input_nodes: list[str],
    output_nodes: list[str],
    base_conduction_velocity: float = 1.0,
    threshold: float = 1.0,
    perturbations: list[dict] | None = None,
    n_trials: int = DEFAULT_N_TRIALS,
    noise_std: float = DEFAULT_NOISE_STD,
    slowdown_fn: SlowdownFn = linear_slowdown,
    threshold_fn: ThresholdFn = linear_threshold_increase,
    seed: int | None = None,
) -> dict:
    """Healthy vs. damaged trial-based comparison — the stochastic counterpart
    to `mbsim.metrics.compare`. Same perturbation targeting, but each side is
    `n_trials` noisy runs instead of one deterministic run, so
    `healthy_weber_fraction`/`damaged_weber_fraction` are actual measured
    variability, not a single-point ratio.
    """
    perturbations = perturbations or []
    edge_severity = per_edge_velocity_severity(graph, perturbations)
    node_severity = per_node_threshold_severity(graph, perturbations)
    edge_velocity = {
        edge: damaged_conduction_velocity(base_conduction_velocity, severity, slowdown_fn)
        for edge, severity in edge_severity.items()
    }
    node_threshold = {
        node: damaged_threshold(threshold, severity, threshold_fn) for node, severity in node_severity.items()
    }

    healthy_samples, healthy_stats = run_trials(
        graph,
        input_nodes,
        output_nodes,
        base_conduction_velocity,
        threshold,
        n_trials=n_trials,
        noise_std=noise_std,
        seed=seed,
    )
    damaged_samples, damaged_stats = run_trials(
        graph,
        input_nodes,
        output_nodes,
        base_conduction_velocity,
        threshold,
        edge_velocity=edge_velocity,
        node_threshold=node_threshold,
        n_trials=n_trials,
        noise_std=noise_std,
        seed=None if seed is None else seed + 1,
    )
    return {
        "healthy_samples": healthy_samples,
        "healthy_stats": healthy_stats,
        "healthy_weber_fraction": mean_weber_fraction(healthy_stats),
        "damaged_samples": damaged_samples,
        "damaged_stats": damaged_stats,
        "damaged_weber_fraction": mean_weber_fraction(damaged_stats),
    }
