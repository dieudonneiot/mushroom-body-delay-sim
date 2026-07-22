from pathlib import Path

from mbsim.graph import build_graph
from mbsim.io import load_raw_data
from mbsim.mushroom_body import extract_mb_subgraph
from mbsim.simulation import simulate

FIXTURE_DIR = Path(__file__).parent.parent / "data" / "fixtures"
ROLES = {"input": ["PN"], "relay": ["KC"], "output": ["MBON"]}


def _fixture_graph():
    connections, classification = load_raw_data(FIXTURE_DIR)
    edge_df, node_roles = extract_mb_subgraph(connections, classification, ROLES)
    return build_graph(edge_df, node_roles)


def test_input_nodes_fire_at_time_zero():
    graph = _fixture_graph()
    fire_times = simulate(graph, ["PN1", "PN2", "PN3"], conduction_velocity=1.0, threshold=1.0)
    assert fire_times["PN1"] == 0.0
    assert fire_times["PN2"] == 0.0
    assert fire_times["PN3"] == 0.0


def test_signal_reaches_all_downstream_nodes():
    graph = _fixture_graph()
    fire_times = simulate(graph, ["PN1", "PN2", "PN3"], conduction_velocity=1.0, threshold=1.0)
    assert set(fire_times) == set(graph.nodes)


def test_fire_times_increase_downstream():
    graph = _fixture_graph()
    fire_times = simulate(graph, ["PN1", "PN2", "PN3"], conduction_velocity=1.0, threshold=1.0)
    assert fire_times["KC1"] > fire_times["PN1"]
    assert fire_times["MBON1"] > fire_times["KC1"]


def test_lower_conduction_velocity_increases_delay():
    graph = _fixture_graph()
    fast = simulate(graph, ["PN1", "PN2", "PN3"], conduction_velocity=1.0, threshold=1.0)
    slow = simulate(graph, ["PN1", "PN2", "PN3"], conduction_velocity=0.5, threshold=1.0)
    for node in ("KC1", "MBON1", "MBON2"):
        assert slow[node] > fast[node]
