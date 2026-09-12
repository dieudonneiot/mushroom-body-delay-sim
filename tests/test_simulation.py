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


def test_edge_velocity_override_only_affects_that_edge():
    graph = _fixture_graph()
    baseline = simulate(graph, ["PN1", "PN2", "PN3"], conduction_velocity=1.0, threshold=1.0)
    overridden = simulate(
        graph,
        ["PN1", "PN2", "PN3"],
        conduction_velocity=1.0,
        threshold=1.0,
        edge_velocity={("PN1", "KC1"): 0.1},
    )
    assert overridden["KC1"] > baseline["KC1"]
    # KC2 is reached via a different edge (PN1->KC2, not overridden) — unaffected.
    assert overridden["KC2"] == baseline["KC2"]


def test_zero_velocity_edge_makes_the_only_downstream_node_unreached():
    """A fully-blocked edge (conduction_velocity == 0, reachable via a 100%
    intensity Tau/Amyloid perturbation) must exclude the node it was the only
    path to, not report it reached at some astronomically large fire time."""
    graph = _fixture_graph()
    fire_times = simulate(
        graph, ["PN1", "PN2", "PN3"], conduction_velocity=1.0, threshold=1.0, edge_velocity={("PN1", "KC1"): 0.0}
    )
    assert "KC1" not in fire_times  # KC1's only incoming edge is PN1->KC1
    assert "KC2" in fire_times  # reached via a different, unaffected edge


def test_node_threshold_override_only_delays_that_node():
    graph = _fixture_graph()
    baseline = simulate(graph, ["PN1", "PN2", "PN3"], conduction_velocity=1.0, threshold=1.0)
    overridden = simulate(
        graph,
        ["PN1", "PN2", "PN3"],
        conduction_velocity=1.0,
        threshold=1.0,
        node_threshold={"MBON1": 2.0},
    )
    assert overridden["MBON1"] > baseline["MBON1"]
    assert overridden["MBON2"] == baseline["MBON2"]
