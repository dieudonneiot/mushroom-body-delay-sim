from pathlib import Path

from mbsim.damage import damaged_conduction_velocity, linear_slowdown
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


def test_compare_reports_positive_deviation_for_nonzero_severity():
    graph = _fixture_graph()
    result = compare(
        graph,
        input_nodes=["PN1", "PN2", "PN3"],
        output_nodes=["MBON1", "MBON2"],
        base_conduction_velocity=1.0,
        threshold=1.0,
        severity=0.3,
    )
    assert len(result.df) == 2
    assert (result.df["pct_deviation"] > 0).all()
    assert result.summary["mean_pct_deviation"] > 0
    assert set(result.healthy_fire_times) == set(graph.nodes)
    assert set(result.damaged_fire_times) == set(graph.nodes)


def test_deviation_grows_with_severity():
    graph = _fixture_graph()
    low = compare(graph, ["PN1", "PN2", "PN3"], ["MBON1", "MBON2"], severity=0.1)
    high = compare(graph, ["PN1", "PN2", "PN3"], ["MBON1", "MBON2"], severity=0.6)
    assert high.summary["mean_pct_deviation"] > low.summary["mean_pct_deviation"]
