from pathlib import Path

from mbsim.graph import build_graph, sanity_report
from mbsim.io import load_raw_data
from mbsim.mushroom_body import extract_mb_subgraph

FIXTURE_DIR = Path(__file__).parent.parent / "data" / "fixtures"
ROLES = {"input": ["PN"], "relay": ["KC"], "output": ["MBON"]}


def _build_fixture_graph():
    connections, classification = load_raw_data(FIXTURE_DIR)
    edge_df, node_roles = extract_mb_subgraph(connections, classification, ROLES)
    return build_graph(edge_df, node_roles)


def test_fixture_graph_node_and_edge_counts():
    graph = _build_fixture_graph()
    report = sanity_report(graph)

    assert report["n_nodes"] == 11  # 3 PN + 6 KC + 2 MBON
    assert report["n_edges"] == 13
    assert report["role_counts"] == {"input": 3, "relay": 6, "output": 2}
    assert report["n_isolated_nodes"] == 0


def test_edges_carry_synapse_count_weight():
    graph = _build_fixture_graph()
    assert graph.edges["PN1", "KC1"]["weight"] == 12


def test_edges_carry_nt_type_for_targeting():
    """nt_type must survive into the graph so mbsim.targeting can resolve
    GABA-specific perturbations to real edges instead of the whole graph."""
    graph = _build_fixture_graph()
    assert graph.edges["PN1", "KC1"]["nt_type"] == "ACH"


def test_extra_node_ids_force_includes_an_otherwise_unclassified_neuron():
    """APL (and similar neurons with no dedicated classification label) must be
    forceable into the subgraph via extra_node_ids, or no perturbation could
    ever target its edges — see mbsim.targeting's module docstring."""
    connections, classification = load_raw_data(FIXTURE_DIR)
    # "KC1" already exists in the fixture; simulate forcing in an id that
    # wouldn't otherwise match any configured role.
    edge_df, node_roles = extract_mb_subgraph(
        connections, classification, {"input": ["PN"], "output": ["MBON"]}, extra_node_ids=["KC1"]
    )
    assert node_roles["KC1"] == "modulatory"
