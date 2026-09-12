import networkx as nx

from mbsim.targeting import (
    edges_by_neuropil,
    edges_by_nt_type,
    edges_from_nodes,
    resolve_targets,
)


def _graph():
    g = nx.DiGraph()
    g.add_edge("A", "B", nt_type="ACH", neuropil="MB_CA_L")
    g.add_edge("B", "C", nt_type="GABA", neuropil="MB_CA_L")
    g.add_edge("C", "D", nt_type="GABA", neuropil="MB_ML_L")
    g.add_edge("D", "E", nt_type="ACH", neuropil="MB_ML_L")
    return g


def test_edges_by_nt_type_matches_only_that_transmitter():
    g = _graph()
    assert edges_by_nt_type(g, ("GABA",)) == {("B", "C"), ("C", "D")}


def test_edges_by_neuropil_matches_only_that_compartment():
    g = _graph()
    assert edges_by_neuropil(g, ["MB_ML_L"]) == {("C", "D"), ("D", "E")}


def test_edges_from_nodes_matches_only_outgoing_edges():
    g = _graph()
    # C has one incoming edge (B->C) and one outgoing edge (C->D) — only the
    # outgoing one counts, since target_root_ids scopes a neuron's own
    # presynaptic output, not edges other neurons happen to send it.
    assert edges_from_nodes(g, ["C"]) == {("C", "D")}


def test_tau_and_amyloid_default_to_every_edge():
    g = _graph()
    assert resolve_targets(g, {"type": "tau"}) == set(g.edges())
    assert resolve_targets(g, {"type": "amyloid"}) == set(g.edges())


def test_gaba_defaults_to_only_gabaergic_edges():
    g = _graph()
    assert resolve_targets(g, {"type": "gaba"}) == {("B", "C"), ("C", "D")}


def test_gaba_on_a_purely_cholinergic_graph_targets_nothing():
    """Mirrors the bundled demo fixture, which is 100% ACH — GABA legitimately
    has zero effect there, and that must not silently fall back to "all edges"."""
    g = nx.DiGraph()
    g.add_edge("A", "B", nt_type="ACH")
    assert resolve_targets(g, {"type": "gaba"}) == set()


def test_apl_has_no_default_target():
    g = _graph()
    assert resolve_targets(g, {"type": "apl"}) == set()


def test_apl_targets_exactly_the_supplied_root_ids_outgoing_edges():
    g = _graph()
    assert resolve_targets(g, {"type": "apl", "target_root_ids": ["C"]}) == {("C", "D")}


def test_target_root_ids_narrows_a_type_with_a_default():
    g = _graph()
    result = resolve_targets(g, {"type": "tau", "target_root_ids": ["B"]})
    assert result == {("B", "C")}


def test_target_neuropils_narrows_gaba_further():
    g = _graph()
    result = resolve_targets(g, {"type": "gaba", "target_neuropils": ["MB_ML_L"]})
    assert result == {("C", "D")}


def test_edges_by_neuropil_matches_a_multi_neuropil_edge():
    """An edge whose neuropil attribute is a frozenset (build_graph's
    aggregated form for a pair connecting across >1 compartment) must match
    on overlap, not a broken exact-equality check against the set object."""
    g = nx.DiGraph()
    g.add_edge("A", "B", nt_type="ACH", neuropil=frozenset({"MB_CA_L", "MB_ML_L"}))
    g.add_edge("B", "C", nt_type="ACH", neuropil="MB_CA_L")
    assert edges_by_neuropil(g, ["MB_ML_L"]) == {("A", "B")}
    assert edges_by_neuropil(g, ["MB_CA_L"]) == {("A", "B"), ("B", "C")}
