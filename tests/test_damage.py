from pathlib import Path

from mbsim.damage import (
    damaged_conduction_velocity,
    damaged_threshold,
    linear_slowdown,
    linear_threshold_increase,
)
from mbsim.graph import build_graph
from mbsim.io import load_raw_data
from mbsim.metrics import compare
from mbsim.mushroom_body import extract_mb_subgraph

FIXTURE_DIR = Path(__file__).parent.parent / "data" / "fixtures"
ROLES = {"input": ["PN"], "relay": ["KC"], "output": ["MBON"]}


def _fixture_graph():
    connections, classification = load_raw_data(FIXTURE_DIR)
    edge_df, node_roles = extract_mb_subgraph(connections, classification, ROLES)
    return build_graph(edge_df, node_roles)


def test_linear_slowdown_is_clamped_to_unit_interval():
    assert linear_slowdown(-1.0) == 0.0
    assert linear_slowdown(0.5) == 0.5
    assert linear_slowdown(2.0) == 1.0


def test_damaged_velocity_decreases_with_severity():
    v_low = damaged_conduction_velocity(1.0, severity=0.2)
    v_high = damaged_conduction_velocity(1.0, severity=0.8)
    assert v_high < v_low < 1.0


def test_threshold_increase_is_clamped_to_unit_interval():
    assert linear_threshold_increase(-1.0) == 0.0
    assert linear_threshold_increase(0.5) == 0.5
    assert linear_threshold_increase(2.0) == 1.0


def test_damaged_threshold_increases_with_severity():
    t_low = damaged_threshold(1.0, severity=0.2)
    t_high = damaged_threshold(1.0, severity=0.8)
    assert t_high > t_low > 1.0


def test_compare_reports_positive_deviation_for_a_tau_perturbation():
    graph = _fixture_graph()
    result = compare(
        graph,
        input_nodes=["PN1", "PN2", "PN3"],
        output_nodes=["MBON1", "MBON2"],
        base_conduction_velocity=1.0,
        threshold=1.0,
        perturbations=[{"type": "tau", "intensity": 30.0}],
    )
    assert len(result.df) == 2
    assert (result.df["pct_deviation"] > 0).all()
    assert result.summary["mean_pct_deviation"] > 0
    assert result.summary["n_edges_velocity_targeted"] == result.summary["n_edges_total"]
    assert set(result.healthy_fire_times) == set(graph.nodes)
    assert set(result.damaged_fire_times) == set(graph.nodes)


def test_deviation_grows_with_tau_intensity():
    graph = _fixture_graph()
    low = compare(graph, ["PN1", "PN2", "PN3"], ["MBON1", "MBON2"], perturbations=[{"type": "tau", "intensity": 10.0}])
    high = compare(graph, ["PN1", "PN2", "PN3"], ["MBON1", "MBON2"], perturbations=[{"type": "tau", "intensity": 60.0}])
    assert high.summary["mean_pct_deviation"] > low.summary["mean_pct_deviation"]


def test_gaba_has_no_effect_on_the_purely_cholinergic_fixture():
    """The bundled demo fixture has no GABAergic edges (see data/fixtures/README) —
    a GABA perturbation must legitimately resolve to zero targeted nodes/effect
    here, not silently fall back to a global effect."""
    graph = _fixture_graph()
    result = compare(
        graph,
        ["PN1", "PN2", "PN3"],
        ["MBON1", "MBON2"],
        perturbations=[{"type": "gaba", "intensity": 50.0}],
    )
    assert result.summary["n_nodes_threshold_targeted"] == 0
    assert (result.df["pct_deviation"] == 0).all()


def test_threshold_channel_is_independent_of_velocity_channel():
    """A pure threshold-channel perturbation (APL, targeted via target_root_ids
    since it has no connectome label) must not touch conduction velocity at
    all. target_root_ids scopes a neuron's own *outgoing* synapses (see
    targeting.edges_from_nodes), so targeting "KC1" (whose only outgoing edge
    feeds MBON1) raises MBON1's threshold, not KC1's own. MBON1 has three
    converging inputs (KC1/KC2/KC3), so doubling its threshold means it now
    needs a second convergent input before firing instead of just the first,
    making the delay directly observable rather than dropping the signal."""
    graph = _fixture_graph()
    result = compare(
        graph,
        ["PN1", "PN2", "PN3"],
        ["MBON1", "MBON2"],
        perturbations=[{"type": "apl", "intensity": 100.0, "target_root_ids": ["KC1"]}],
    )
    assert result.summary["n_edges_velocity_targeted"] == 0
    assert result.summary["n_nodes_threshold_targeted"] == 1
    assert result.healthy_fire_times["MBON1"] < result.damaged_fire_times["MBON1"]
    assert result.healthy_fire_times["MBON2"] == result.damaged_fire_times["MBON2"]
