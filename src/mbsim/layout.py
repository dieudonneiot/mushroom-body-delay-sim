"""Shared node layout and role color scheme for both the matplotlib and Plotly renderers."""

import networkx as nx

ROLE_COLORS = {"input": "#2ca02c", "relay": "#1f77b4", "output": "#ff7f0e"}
DEFAULT_ROLE_COLOR = "#999999"


def layered_layout(graph: nx.DiGraph) -> dict[str, tuple[float, float]]:
    """Left-to-right layout by role (input -> relay -> output) instead of a generic spring layout."""
    role_order = {"input": 0, "relay": 1, "output": 2}
    columns: dict[int, list[str]] = {}
    for node, data in graph.nodes(data=True):
        col = role_order.get(data.get("role"), 1)
        columns.setdefault(col, []).append(node)

    pos = {}
    for col, nodes in columns.items():
        nodes = sorted(nodes)
        for i, node in enumerate(nodes):
            y = i - (len(nodes) - 1) / 2
            pos[node] = (col, y)
    return pos
