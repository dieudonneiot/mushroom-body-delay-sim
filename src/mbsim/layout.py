"""Shared node layout and role color scheme for both the matplotlib and Plotly renderers."""

import hashlib

import networkx as nx

ROLE_COLORS = {"input": "#2ca02c", "relay": "#1f77b4", "output": "#ff7f0e", "modulatory": "#9467bd"}
DEFAULT_ROLE_COLOR = "#999999"
COLUMN_BAND_WIDTH = 0.35


def _stable_jitter(node: str, width: float) -> float:
    """Deterministic pseudo-random offset in [-width/2, width/2], stable across runs
    (unlike hash(), which is randomized per-process for strings)."""
    digest = hashlib.sha256(str(node).encode()).digest()
    frac = int.from_bytes(digest[:4], "big") / 0xFFFFFFFF
    return (frac - 0.5) * width


def layered_layout(graph: nx.DiGraph, band_width: float = COLUMN_BAND_WIDTH) -> dict[str, tuple[float, float]]:
    """Left-to-right layout by role (input -> relay -> output) instead of a generic spring layout.

    Each column's y-extent is normalized to roughly [-0.5, 0.5] regardless of how many
    nodes it holds, so a column of 5000 Kenyon cells doesn't dwarf a column of 100 MBONs
    and turn the whole figure into a giant diamond — every column renders at the same
    height, just denser. Nodes are also given a small deterministic horizontal jitter
    around their column's x position, so each column renders as a visible band of dots
    rather than a razor-thin, hard-to-read line.
    """
    role_order = {"input": 0, "relay": 1, "output": 2}
    columns: dict[int, list[str]] = {}
    for node, data in graph.nodes(data=True):
        col = role_order.get(data.get("role"), 1)
        columns.setdefault(col, []).append(node)

    pos = {}
    for col, nodes in columns.items():
        nodes = sorted(nodes)
        n = len(nodes)
        for i, node in enumerate(nodes):
            y = (i - (n - 1) / 2) / n if n > 1 else 0.0
            x = col + _stable_jitter(node, band_width)
            pos[node] = (x, y)
    return pos


def marker_size(n_nodes: int) -> float:
    """Node marker size (diameter-ish, in the caller's units), scaled down for large
    graphs so thousands of overlapping markers don't render as a solid blob."""
    if n_nodes <= 60:
        return 16.0
    return max(3.0, min(16.0, 900.0 / n_nodes))


def show_node_labels(n_nodes: int) -> bool:
    """Whether to always draw node-id text labels — off for large graphs, where
    thousands of labels are unreadable and expensive to render; hover text (Plotly)
    or omission (matplotlib) covers per-node detail instead."""
    return n_nodes <= 60


def edge_style(n_edges: int) -> tuple[float, float, float]:
    """(min_width, max_width, opacity) for edges, scaled down for large graphs so tens
    of thousands of overlapping lines read as a density gradient instead of a solid fill."""
    if n_edges <= 200:
        return 0.5, 4.0, 0.6
    if n_edges <= 5000:
        return 0.3, 1.5, 0.15
    return 0.15, 0.6, 0.03
