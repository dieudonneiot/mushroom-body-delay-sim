"""Build the Mushroom Body pathway as a NetworkX directed graph."""

from collections import Counter

import networkx as nx
import pandas as pd


def build_graph(edge_df: pd.DataFrame, node_roles: dict[str, str]) -> nx.DiGraph:
    graph = nx.DiGraph()
    for node_id, role in node_roles.items():
        graph.add_node(node_id, role=role)
    # nt_type/neuropil are optional (present in the real Codex export and the
    # demo fixture, but not required by mbsim.io) — carried through as edge
    # attributes so mbsim.targeting can resolve perturbations like GABA to
    # the specific edges they biologically affect, instead of the whole graph.
    optional_attrs = [c for c in ("nt_type", "neuropil") if c in edge_df.columns]
    # A real Codex export has one row per (pre, post, neuropil) triple, so the
    # same neuron pair legitimately appears more than once whenever it
    # connects across more than one MB compartment. Group first and aggregate
    # rather than calling add_edge() once per row — the latter lets each
    # later row for the same pair silently overwrite (not sum) the earlier
    # row's weight/attrs, undercounting synapse strength.
    for (pre_id, post_id), rows in edge_df.groupby(["pre_id", "post_id"], sort=False):
        attrs = {}
        for attr in optional_attrs:
            values = pd.unique(rows[attr].dropna())
            # Keep a plain scalar in the common single-row case (what every
            # existing caller/test expects); only a genuinely multi-valued
            # pair (e.g. differing nt_type/neuropil across compartments)
            # becomes a frozenset — mbsim.targeting's edge filters handle both.
            attrs[attr] = values[0] if len(values) <= 1 else frozenset(values)
        graph.add_edge(pre_id, post_id, weight=int(rows["syn_count"].sum()), **attrs)
    return graph


def sanity_report(graph: nx.DiGraph) -> dict:
    role_counts = Counter(nx.get_node_attributes(graph, "role").values())
    isolated = list(nx.isolates(graph))
    report = {
        "n_nodes": graph.number_of_nodes(),
        "n_edges": graph.number_of_edges(),
        "role_counts": dict(role_counts),
        "n_isolated_nodes": len(isolated),
        "isolated_nodes": isolated,
    }
    return report


def print_sanity_report(graph: nx.DiGraph) -> None:
    report = sanity_report(graph)
    print(f"Mushroom Body graph: {report['n_nodes']} nodes, {report['n_edges']} edges")
    print(f"  Role breakdown: {report['role_counts']}")
    if report["n_isolated_nodes"]:
        print(
            f"  Warning: {report['n_isolated_nodes']} isolated node(s) with no MB-pathway "
            f"edges: {report['isolated_nodes'][:10]}"
            + (" ..." if report["n_isolated_nodes"] > 10 else "")
        )
