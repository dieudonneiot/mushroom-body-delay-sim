"""Which graph edges each perturbation type's damage should apply to.

Prior versions of this pipeline applied every perturbation as one global
scalar (a single conduction-velocity or firing-threshold multiplier shared by
every edge/node in the graph). That made Tau, Amyloid, GABA, and APL
functionally interchangeable — a real Codex connectome carries the data to
target them more specifically, so this module resolves each perturbation to
the actual subset of edges it should touch:

- Tau: hyperphosphorylated tangles disrupt axonal transport broadly, with no
  single connectome field marking "which axons" — targets every edge.
- Amyloid: plaque buildup impairing synaptic transmission is likewise
  modeled as broad by default (targets every edge), but can be narrowed to
  specific Mushroom Body compartments via `target_neuropils` (e.g.
  `["MB_CA_L"]` for the calyx) if the medical team wants compartment-
  specific plaque deposition instead of a brain-wide effect.
- GABA: the real Codex "Connections (Filtered)" export carries a per-edge
  `nt_type` column (ACH/GABA/GLUT/OCT/SER/DA in the FAFB dataset) — GABA
  dysfunction targets exactly the edges whose `nt_type == "GABA"`. On data
  without that column (or a subgraph with no GABAergic edges, like the
  bundled demo fixture, which is purely cholinergic) this legitimately
  resolves to zero edges: that is the correct, honest result, not a bug.
- APL (Anterior Paired Lateral): a single, individually-named neuron pair
  providing MB-wide feedback inhibition — but verified against the real
  FAFB `classification.csv` export, there is no `class`/`sub_class` value
  identifying it (the classification file's granularity stops at coarser
  categories like `Kenyon_Cell`/`MBON`/`MBIN`). It cannot be targeted from
  bulk-exported data alone. APL therefore has **no default target** — it
  resolves to zero edges unless the medical team looks it up by name on
  codex.flywire.ai (Codex's neuron search does support per-name lookup even
  though the bulk classification export doesn't) and supplies its root_id
  via `target_root_ids`. `mushroom_body.extract_mb_subgraph`'s
  `extra_node_ids` parameter must also be used to force that neuron's node
  into the pathway subgraph, since its unlabeled `class` would otherwise be
  filtered out by the normal role-based extraction.

Any perturbation may optionally include `target_root_ids` and/or
`target_neuropils` to narrow its default target set (an override always
narrows an existing default via intersection; for a type with no default,
i.e. APL, an override defines the target set directly rather than
intersecting with the empty set).
"""

import networkx as nx


def all_edges(graph: nx.DiGraph) -> set[tuple[str, str]]:
    return set(graph.edges())


def _matches_any(value, wanted: set) -> bool:
    """True if `value` (a plain scalar, or a frozenset for an edge whose
    attribute genuinely varies across the multiple connectome rows
    mbsim.graph.build_graph aggregated into it) overlaps `wanted`."""
    if isinstance(value, (frozenset, set)):
        return bool(value & wanted)
    return value in wanted


def edges_by_nt_type(graph: nx.DiGraph, nt_types: tuple[str, ...]) -> set[tuple[str, str]]:
    wanted = set(nt_types)
    return {(u, v) for u, v, data in graph.edges(data=True) if _matches_any(data.get("nt_type"), wanted)}


def edges_by_neuropil(graph: nx.DiGraph, neuropils: list[str]) -> set[tuple[str, str]]:
    wanted = set(neuropils)
    return {(u, v) for u, v, data in graph.edges(data=True) if _matches_any(data.get("neuropil"), wanted)}


def edges_from_nodes(graph: nx.DiGraph, node_ids: list[str]) -> set[tuple[str, str]]:
    """Edges *outgoing from* the given nodes — i.e. that neuron's own synapses
    onto its targets. Deliberately one-directional, not "any edge touching
    this node": for a specific-neuron override (APL's `target_root_ids`, or
    narrowing Tau/Amyloid to one neuron) the biologically relevant scope is
    that neuron's own presynaptic output — axonal-transport/synaptic-release
    dysfunction (Tau/Amyloid) or lost inhibitory output (APL) both originate
    at the neuron's outgoing terminals, not at whatever unrelated edges
    happen to end there from other presynaptic partners."""
    wanted = {str(n) for n in node_ids}
    return {(u, v) for u, v in graph.edges() if str(u) in wanted}


# Default biological target for each perturbation type; None means "no default
# scope — must be narrowed via target_root_ids/target_neuropils, otherwise
# resolves to zero edges" (currently only APL, see module docstring).
DEFAULT_TARGET_FNS = {
    "tau": all_edges,
    "amyloid": all_edges,
    "gaba": lambda graph: edges_by_nt_type(graph, ("GABA",)),
    "apl": None,
}


def resolve_targets(graph: nx.DiGraph, perturbation: dict) -> set[tuple[str, str]]:
    """The actual set of edges `perturbation` should apply damage to."""
    default_fn = DEFAULT_TARGET_FNS.get(perturbation.get("type"))
    targets = default_fn(graph) if default_fn is not None else None

    root_ids = perturbation.get("target_root_ids")
    if root_ids:
        by_root = edges_from_nodes(graph, root_ids)
        targets = by_root if targets is None else (targets & by_root)

    neuropils = perturbation.get("target_neuropils")
    if neuropils:
        by_neuropil = edges_by_neuropil(graph, neuropils)
        targets = by_neuropil if targets is None else (targets & by_neuropil)

    return targets if targets is not None else set()
