"""Build the Mushroom Body pathway as a NetworkX directed graph."""

from collections import Counter

import networkx as nx
import pandas as pd


def build_graph(edge_df: pd.DataFrame, node_roles: dict[str, str]) -> nx.DiGraph:
    graph = nx.DiGraph()
    for node_id, role in node_roles.items():
        graph.add_node(node_id, role=role)
    for row in edge_df.itertuples():
        graph.add_edge(row.pre_id, row.post_id, weight=int(row.syn_count))
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
