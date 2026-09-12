import networkx as nx
import pytest

from mbsim.perturbations import PERTURBATION_TYPES, per_edge_velocity_severity, per_node_threshold_severity
from mbsim.targeting import DEFAULT_TARGET_FNS


def test_every_perturbation_type_has_a_targeting_entry():
    """Every key in PERTURBATION_TYPES (what the UI lets a user select) must
    have a corresponding entry in targeting.DEFAULT_TARGET_FNS (what that
    type actually affects) — otherwise a type registered in only one dict
    would look like a fully working, selectable perturbation while silently
    having zero effect everywhere, with nothing to catch the mismatch."""
    assert set(PERTURBATION_TYPES) <= set(DEFAULT_TARGET_FNS)


def _graph():
    g = nx.DiGraph()
    g.add_edge("A", "B", nt_type="ACH")
    g.add_edge("B", "C", nt_type="GABA")
    return g


def test_empty_perturbations_give_no_targeted_edges_or_nodes():
    g = _graph()
    assert per_edge_velocity_severity(g, []) == {}
    assert per_node_threshold_severity(g, []) == {}


def test_tau_applies_its_intensity_to_every_edge():
    g = _graph()
    severity = per_edge_velocity_severity(g, [{"type": "tau", "intensity": 18.0}])
    assert severity == pytest.approx({("A", "B"): 0.18, ("B", "C"): 0.18})


def test_gaba_only_applies_to_gabaergic_edges_postsynaptic_node():
    g = _graph()
    severity = per_node_threshold_severity(g, [{"type": "gaba", "intensity": 12.0}])
    # Only "C" (postsynaptic end of the one GABAergic edge) is affected, not "B".
    assert severity == {"C": 0.12}


def test_two_velocity_perturbations_on_the_same_edge_combine_multiplicatively():
    g = nx.DiGraph()
    g.add_edge("A", "B", nt_type="ACH")
    severity = per_edge_velocity_severity(
        g,
        [
            {"type": "tau", "intensity": 18.0},
            {"type": "amyloid", "intensity": 10.0},
        ],
    )
    expected = 1.0 - (1.0 - 0.18) * (1.0 - 0.10)
    assert abs(severity[("A", "B")] - expected) < 1e-9
    assert abs(severity[("A", "B")] - 0.28) > 1e-9  # not simple addition


def test_velocity_and_threshold_channels_stay_independent():
    """Tau (velocity) on an edge must not appear in the threshold map, and GABA
    (threshold) must not appear in the velocity map."""
    g = _graph()
    perturbations = [
        {"type": "tau", "intensity": 40.0},
        {"type": "gaba", "intensity": 25.0},
    ]
    edge_severity = per_edge_velocity_severity(g, perturbations)
    node_severity = per_node_threshold_severity(g, perturbations)
    assert edge_severity == {("A", "B"): 0.40, ("B", "C"): 0.40}
    assert node_severity == {"C": 0.25}


def test_zero_intensity_and_unknown_type_are_ignored():
    g = _graph()
    perturbations = [
        {"type": "tau", "intensity": 0.0},
        {"type": "not_a_real_type", "intensity": 50.0},
    ]
    assert per_edge_velocity_severity(g, perturbations) == {}


def test_apl_without_target_root_ids_affects_nothing():
    g = _graph()
    assert per_node_threshold_severity(g, [{"type": "apl", "intensity": 90.0}]) == {}


def test_apl_with_target_root_ids_affects_its_postsynaptic_target_not_itself():
    """target_root_ids=["B"] scopes B's own outgoing synapse (B->C) — the
    threshold rise lands on C (what loses APL's inhibition), not on B itself."""
    g = _graph()
    severity = per_node_threshold_severity(
        g, [{"type": "apl", "intensity": 30.0, "target_root_ids": ["B"]}]
    )
    assert severity == pytest.approx({"C": 0.30})
