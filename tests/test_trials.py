import random
import statistics
from pathlib import Path

from mbsim.graph import build_graph
from mbsim.io import load_raw_data
from mbsim.mushroom_body import extract_mb_subgraph
from mbsim.trials import _jittered_velocity, compare_trials, mean_weber_fraction, run_trials

FIXTURE_DIR = Path(__file__).parent.parent / "data" / "fixtures"
ROLES = {"input": ["PN"], "relay": ["KC"], "output": ["MBON"]}


def _fixture_graph():
    connections, classification = load_raw_data(FIXTURE_DIR)
    edge_df, node_roles = extract_mb_subgraph(connections, classification, ROLES)
    return build_graph(edge_df, node_roles)


def test_zero_noise_gives_identical_samples_and_zero_cv():
    graph = _fixture_graph()
    _, stats = run_trials(
        graph, ["PN1", "PN2", "PN3"], ["MBON1", "MBON2"], n_trials=10, noise_std=0.0, seed=1
    )
    for node_stats in stats.values():
        assert node_stats["cv"] == 0.0


def test_nonzero_noise_gives_positive_variability():
    graph = _fixture_graph()
    _, stats = run_trials(
        graph, ["PN1", "PN2", "PN3"], ["MBON1", "MBON2"], n_trials=50, noise_std=0.2, seed=1
    )
    assert all(node_stats["cv"] > 0 for node_stats in stats.values())


def test_run_trials_is_reproducible_with_a_seed():
    graph = _fixture_graph()
    samples_a, _ = run_trials(graph, ["PN1", "PN2", "PN3"], ["MBON1"], n_trials=20, noise_std=0.15, seed=42)
    samples_b, _ = run_trials(graph, ["PN1", "PN2", "PN3"], ["MBON1"], n_trials=20, noise_std=0.15, seed=42)
    assert samples_a == samples_b


def test_mean_weber_fraction_averages_across_nodes():
    stats = {"A": {"cv": 0.1}, "B": {"cv": 0.3}, "C": {"cv": None}}
    assert abs(mean_weber_fraction(stats) - 0.2) < 1e-9


def test_mean_weber_fraction_is_none_when_no_node_has_enough_trials():
    assert mean_weber_fraction({"A": {"cv": None}}) is None


def test_jittered_velocity_is_mean_preserving_across_noise_levels():
    """E[_jittered_velocity(base, noise_std)] must stay ~= base for any
    noise_std — a bare lognormvariate(0, sigma) has E[x] = exp(sigma^2/2) and
    would systematically inflate the mean as noise_std grows, confounding
    injected variability with average network speed."""
    rng = random.Random(0)
    base = 2.0
    for noise_std in (0.1, 0.3, 0.5):
        samples = [_jittered_velocity(base, noise_std, rng) for _ in range(200_000)]
        assert abs(statistics.mean(samples) - base) / base < 0.01


def test_run_trials_gives_independent_noise_per_edge_not_one_shared_draw():
    """Two output nodes reached via disjoint edges from the same input must be
    able to diverge trial-to-trial — previously every edge without an
    explicit damage override shared one draw per trial (the global fallback
    conduction_velocity), so all such edges moved in lockstep and the ratio
    between any two nodes' arrival times was constant across every trial."""
    graph = _fixture_graph()
    samples, _ = run_trials(graph, ["PN1", "PN2", "PN3"], ["MBON1", "MBON2"], n_trials=30, noise_std=0.2, seed=3)
    ratios = {a / b for a, b in zip(samples["MBON1"], samples["MBON2"])}
    assert len(ratios) > 1  # would be a single constant ratio under shared-noise behavior


def test_compare_trials_damaged_side_reflects_targeted_perturbations():
    graph = _fixture_graph()
    result = compare_trials(
        graph,
        ["PN1", "PN2", "PN3"],
        ["MBON1", "MBON2"],
        perturbations=[{"type": "tau", "intensity": 40.0}],
        n_trials=15,
        noise_std=0.1,
        seed=7,
    )
    healthy_means = {n: s["mean"] for n, s in result["healthy_stats"].items() if s["mean"] is not None}
    damaged_means = {n: s["mean"] for n, s in result["damaged_stats"].items() if s["mean"] is not None}
    for node in healthy_means:
        assert damaged_means[node] > healthy_means[node]
