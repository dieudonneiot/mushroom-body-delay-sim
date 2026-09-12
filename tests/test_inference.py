from pathlib import Path

import numpy as np
import pytest

from mbsim.graph import build_graph
from mbsim.inference import (
    abc_reject,
    combined_severity,
    default_prior_sampler,
    run_sbc,
    sbc_rank_uniformity_pvalue,
    simulate_patient_profile,
    summary_stats,
    theta_to_perturbations,
)
from mbsim.io import load_raw_data
from mbsim.mushroom_body import extract_mb_subgraph

FIXTURE_DIR = Path(__file__).parent.parent / "data" / "fixtures"
ROLES = {"input": ["PN"], "relay": ["KC"], "output": ["MBON"]}
INPUT_NODES = ["PN1", "PN2", "PN3"]
OUTPUT_NODES = ["MBON1", "MBON2"]


def _fixture_graph():
    connections, classification = load_raw_data(FIXTURE_DIR)
    edge_df, node_roles = extract_mb_subgraph(connections, classification, ROLES)
    return build_graph(edge_df, node_roles)


def test_theta_to_perturbations_gives_amyloid_a_narrower_scope_than_tau():
    """The tau/amyloid identifiability fix (module docstring point 1): tau
    stays brain-wide, amyloid is narrowed via target_neuropils, so the two
    are no longer mathematically interchangeable in the forward model."""
    perturbations = theta_to_perturbations({"tau": 30.0, "amyloid": 20.0})
    tau_entry = next(p for p in perturbations if p["type"] == "tau")
    amyloid_entry = next(p for p in perturbations if p["type"] == "amyloid")
    assert "target_neuropils" not in tau_entry
    assert amyloid_entry["target_neuropils"]


def test_theta_to_perturbations_omits_zero_intensity_dimensions():
    assert theta_to_perturbations({"tau": 0.0, "amyloid": 0.0}) == []


def test_combined_severity_matches_independent_multiplicative_combination():
    theta = {"tau": 20.0, "amyloid": 10.0}
    expected = 1.0 - (1.0 - 0.20) * (1.0 - 0.10)
    assert combined_severity(theta) == pytest.approx(expected)


def test_tau_and_amyloid_now_produce_different_profiles_at_equal_intensity():
    """Before the identifiability fix, equal-intensity tau vs. amyloid were
    exactly interchangeable (same channel/scope) — with amyloid narrowed to
    the calyx compartment, the two must now differ on this graph, where tau's
    all-edge scope also covers the non-calyx KC->MBON edges amyloid excludes."""
    graph = _fixture_graph()
    tau_profile = simulate_patient_profile(
        graph, INPUT_NODES, OUTPUT_NODES, {"tau": 50.0, "amyloid": 0.0}, n_trials=20, seed=1
    )
    amyloid_profile = simulate_patient_profile(
        graph, INPUT_NODES, OUTPUT_NODES, {"tau": 0.0, "amyloid": 50.0}, n_trials=20, seed=1
    )
    tau_dev = tau_profile["per_interval"][5.0]["mean_pct_deviation"]
    amyloid_dev = amyloid_profile["per_interval"][5.0]["mean_pct_deviation"]
    assert tau_dev != pytest.approx(amyloid_dev, rel=1e-6)


def test_healthy_theta_gives_approximately_zero_deviation():
    graph = _fixture_graph()
    profile = simulate_patient_profile(graph, INPUT_NODES, OUTPUT_NODES, {"tau": 0.0, "amyloid": 0.0}, n_trials=1, noise_std=0.0, seed=0)
    assert profile["per_interval"][5.0]["mean_pct_deviation"] == pytest.approx(0.0, abs=1e-6)


def test_higher_severity_gives_larger_mean_deviation():
    graph = _fixture_graph()
    mild = simulate_patient_profile(graph, INPUT_NODES, OUTPUT_NODES, {"tau": 20.0, "amyloid": 0.0}, n_trials=1, noise_std=0.0, seed=0)
    severe = simulate_patient_profile(graph, INPUT_NODES, OUTPUT_NODES, {"tau": 70.0, "amyloid": 0.0}, n_trials=1, noise_std=0.0, seed=0)
    assert severe["per_interval"][5.0]["mean_pct_deviation"] > mild["per_interval"][5.0]["mean_pct_deviation"]


def test_profile_is_flat_across_target_intervals_by_construction():
    """Documented module assumption: delay_ratio does not depend on interval
    length, so every target interval must report identical summary stats."""
    graph = _fixture_graph()
    profile = simulate_patient_profile(
        graph, INPUT_NODES, OUTPUT_NODES, {"tau": 30.0, "amyloid": 10.0}, n_trials=15, noise_std=0.1, seed=2
    )
    deviations = {interval: stats["mean_pct_deviation"] for interval, stats in profile["per_interval"].items()}
    assert len(set(deviations.values())) == 1


def test_fully_blocking_theta_raises_a_clear_error():
    """intensity=100 on tau zeros conduction velocity on every edge — every
    output node becomes unreachable, which must raise, not silently produce
    an astronomical/garbage profile."""
    graph = _fixture_graph()
    with pytest.raises(ValueError, match="not reached|No output node"):
        simulate_patient_profile(graph, INPUT_NODES, OUTPUT_NODES, {"tau": 100.0, "amyloid": 0.0}, n_trials=5, seed=0)


def test_summary_stats_returns_pooled_mean_and_cv():
    graph = _fixture_graph()
    profile = simulate_patient_profile(
        graph, INPUT_NODES, OUTPUT_NODES, {"tau": 30.0, "amyloid": 10.0}, n_trials=15, noise_std=0.1, seed=2
    )
    stats = summary_stats(profile)
    assert stats.shape == (2,)
    assert stats[0] == pytest.approx(profile["per_interval"][5.0]["mean_pct_deviation"])


def test_default_prior_sampler_stays_within_its_documented_range():
    rng = np.random.default_rng(0)
    for _ in range(50):
        theta = default_prior_sampler(rng)
        assert 0.0 <= theta["tau"] <= 80.0
        assert 0.0 <= theta["amyloid"] <= 80.0


def test_abc_reject_recovers_a_known_theta_better_than_the_prior_mean():
    """A minimal sanity check that ABC concentrates near the truth rather than
    just reproducing the prior. `default_prior_sampler`'s U(0,80) x U(0,80)
    prior has a combined-severity mean of ~0.64 by construction (E[1-tau/100]
    = E[1-amyloid/100] = 0.6, so E[c] = 1-0.6*0.6 = 0.64) — deliberately pick
    a true theta far below that (c=0.1) so a meaningful pull toward the truth
    is unambiguous rather than a coincidence of where the prior happens to be
    centered."""
    graph = _fixture_graph()
    true_theta = {"tau": 10.0, "amyloid": 0.0}
    observed_profile = simulate_patient_profile(
        graph, INPUT_NODES, OUTPUT_NODES, true_theta, n_trials=20, noise_std=0.05, seed=10
    )
    observed_stats = summary_stats(observed_profile)

    def forward_fn(theta, rng):
        profile = simulate_patient_profile(
            graph, INPUT_NODES, OUTPUT_NODES, theta, n_trials=3, noise_std=0.05, seed=int(rng.integers(0, 2**31 - 1))
        )
        return summary_stats(profile)

    result = abc_reject(observed_stats, default_prior_sampler, forward_fn, n_sims=600, accept_quantile=0.05, seed=5)
    true_c = combined_severity(true_theta)
    accepted_c = np.mean([combined_severity(t) for t in result["accepted_theta"]])

    prior_mean_c = 0.64  # E[c] under default_prior_sampler, derived above
    assert abs(accepted_c - true_c) < abs(prior_mean_c - true_c)


def test_run_sbc_returns_one_rank_per_repetition():
    graph = _fixture_graph()
    result = run_sbc(
        graph,
        INPUT_NODES,
        OUTPUT_NODES,
        n_repetitions=5,
        n_trials_observed=5,
        n_sims_per_repetition=100,
        n_trials_per_sim=2,
        accept_quantile=0.1,
        seed=0,
    )
    assert result["n_repetitions"] == 5
    assert len(result["ranks"]) == 5
    for r in result["ranks"]:
        assert 0 <= r["rank"] <= r["n_accepted"]


def test_sbc_rank_uniformity_pvalue_is_a_probability():
    graph = _fixture_graph()
    result = run_sbc(
        graph,
        INPUT_NODES,
        OUTPUT_NODES,
        n_repetitions=8,
        n_trials_observed=5,
        n_sims_per_repetition=100,
        n_trials_per_sim=2,
        accept_quantile=0.1,
        seed=1,
    )
    p_value = sbc_rank_uniformity_pvalue(result["ranks"])
    assert 0.0 <= p_value <= 1.0
