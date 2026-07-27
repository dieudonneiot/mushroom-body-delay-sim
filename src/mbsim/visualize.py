"""NetworkX drawings of the Mushroom Body graph: structure and signal-delay overlays."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

from mbsim.layout import ROLE_COLORS, edge_style, layered_layout as _layered_layout, marker_size, show_node_labels


def plot_network_structure(graph: nx.DiGraph, out_path: str, title: str = "Mushroom Body pathway") -> None:
    pos = _layered_layout(graph)
    node_colors = [ROLE_COLORS.get(graph.nodes[n].get("role"), "#999999") for n in graph.nodes]
    weights = [graph.edges[e]["weight"] for e in graph.edges]
    max_w = max(weights) if weights else 1
    min_width, max_width, alpha = edge_style(len(weights))
    edge_widths = [min_width + (max_width - min_width) * (w / max_w) for w in weights]
    node_size = marker_size(graph.number_of_nodes()) ** 2

    fig, ax = plt.subplots(figsize=(9, 6))
    nx.draw_networkx_nodes(graph, pos, node_color=node_colors, node_size=node_size, ax=ax)
    nx.draw_networkx_edges(
        graph,
        pos,
        width=edge_widths,
        edge_color="#888888",
        arrowsize=10,
        arrows=graph.number_of_edges() <= 200,
        alpha=alpha,
        ax=ax,
    )
    if show_node_labels(graph.number_of_nodes()):
        nx.draw_networkx_labels(graph, pos, font_size=7, ax=ax)

    handles = [
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=color, markersize=10, label=role)
        for role, color in ROLE_COLORS.items()
    ]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, 1.02), ncol=3)
    fig.suptitle(title, y=0.98)
    ax.axis("off")
    fig.tight_layout(rect=(0, 0, 1, 0.85))
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_network_delay(
    graph: nx.DiGraph,
    fire_times: dict[str, float],
    out_path: str,
    title: str = "Signal arrival time",
) -> None:
    """Draw the network with node color = arrival time (unreached nodes shown gray)."""
    pos = _layered_layout(graph)
    reached = [t for t in fire_times.values()]
    vmax = max(reached) if reached else 1.0
    node_size = marker_size(graph.number_of_nodes()) ** 2
    _, _, edge_alpha = edge_style(graph.number_of_edges())

    node_colors = [fire_times.get(n, None) for n in graph.nodes]
    unreached = [n for n, c in zip(graph.nodes, node_colors) if c is None]
    plotted_colors = [c if c is not None else 0.0 for c in node_colors]

    fig, ax = plt.subplots(figsize=(9, 6))
    # Plain "plasma", not "plasma_r" — must match plotly_viz.py's colorscale="Plasma"
    # direction so the CLI's static images and the interactive app agree on what a
    # given arrival time looks like.
    nodes = nx.draw_networkx_nodes(
        graph,
        pos,
        node_color=plotted_colors,
        cmap="plasma",
        vmin=0.0,
        vmax=vmax,
        node_size=node_size,
        ax=ax,
    )
    if unreached:
        nx.draw_networkx_nodes(graph, pos, nodelist=unreached, node_color="#cccccc", node_size=node_size, ax=ax)

    nx.draw_networkx_edges(
        graph,
        pos,
        edge_color="#cccccc",
        arrowsize=10,
        arrows=graph.number_of_edges() <= 200,
        alpha=edge_alpha,
        ax=ax,
    )
    if show_node_labels(graph.number_of_nodes()):
        nx.draw_networkx_labels(graph, pos, font_size=7, ax=ax)

    fig.colorbar(nodes, ax=ax, label="Arrival time")
    ax.set_title(title)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
