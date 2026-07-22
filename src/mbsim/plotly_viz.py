"""Interactive Plotly renderings of the Mushroom Body graph, for the Streamlit UI.

Uses the same layered layout / role colors as the static matplotlib report in
visualize.py, but adds hover tooltips and zoom/pan.
"""

from collections import defaultdict

import networkx as nx
import plotly.graph_objects as go

from mbsim.i18n import t
from mbsim.layout import DEFAULT_ROLE_COLOR, ROLE_COLORS, layered_layout

N_EDGE_WIDTH_BUCKETS = 5


def _role_label(role: str | None, lang: str) -> str:
    if role in ("input", "relay", "output"):
        return t(f"role_{role}", lang)
    return t("role_unknown", lang)


def _node_hover_text(graph: nx.DiGraph, node: str, lang: str, fire_time: float | None = None) -> str:
    role = graph.nodes[node].get("role")
    lines = [
        f"{t('hover_id', lang)}: {node}",
        f"{t('hover_role', lang)}: {_role_label(role, lang)}",
        f"{t('hover_in_degree', lang)}: {graph.in_degree(node)}",
        f"{t('hover_out_degree', lang)}: {graph.out_degree(node)}",
    ]
    if fire_time is not None:
        lines.append(f"{t('hover_arrival_time', lang)}: {fire_time:.4f}")
    return "<br>".join(lines)


def _edge_traces(graph: nx.DiGraph, pos: dict) -> list[go.Scattergl]:
    weights = [data["weight"] for _, _, data in graph.edges(data=True)]
    if not weights:
        return []
    min_w, max_w = min(weights), max(weights)

    buckets: dict[int, list[tuple[str, str]]] = defaultdict(list)
    for u, v, data in graph.edges(data=True):
        frac = (data["weight"] - min_w) / (max_w - min_w) if max_w > min_w else 0.5
        bucket = min(int(frac * N_EDGE_WIDTH_BUCKETS), N_EDGE_WIDTH_BUCKETS - 1)
        buckets[bucket].append((u, v))

    traces = []
    for bucket, edges in sorted(buckets.items()):
        xs, ys = [], []
        for u, v in edges:
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            xs += [x0, x1, None]
            ys += [y0, y1, None]
        width = 0.5 + 3.5 * (bucket / max(N_EDGE_WIDTH_BUCKETS - 1, 1))
        traces.append(
            go.Scattergl(
                x=xs,
                y=ys,
                mode="lines",
                line=dict(width=width, color="rgba(150,150,150,0.6)"),
                hoverinfo="skip",
                showlegend=False,
            )
        )
    return traces


def _structure_node_traces(graph: nx.DiGraph, pos: dict, lang: str) -> list[go.Scattergl]:
    roles = sorted({data.get("role") for _, data in graph.nodes(data=True)})
    traces = []
    for role in roles:
        nodes = [n for n, d in graph.nodes(data=True) if d.get("role") == role]
        traces.append(
            go.Scattergl(
                x=[pos[n][0] for n in nodes],
                y=[pos[n][1] for n in nodes],
                mode="markers+text",
                text=nodes,
                textposition="top center",
                textfont=dict(size=9),
                marker=dict(
                    size=16,
                    color=ROLE_COLORS.get(role, DEFAULT_ROLE_COLOR),
                    line=dict(width=1, color="white"),
                ),
                name=_role_label(role, lang),
                hovertext=[_node_hover_text(graph, n, lang) for n in nodes],
                hoverinfo="text",
            )
        )
    return traces


def _delay_node_traces(
    graph: nx.DiGraph, fire_times: dict[str, float], pos: dict, vmax: float | None, lang: str
) -> list[go.Scattergl]:
    reached = [n for n in graph.nodes if n in fire_times]
    unreached = [n for n in graph.nodes if n not in fire_times]
    shared_vmax = vmax if vmax is not None else (max(fire_times.values()) if fire_times else 1.0)

    traces = []
    if reached:
        traces.append(
            go.Scattergl(
                x=[pos[n][0] for n in reached],
                y=[pos[n][1] for n in reached],
                mode="markers+text",
                text=reached,
                textposition="top center",
                textfont=dict(size=9),
                marker=dict(
                    size=16,
                    color=[fire_times[n] for n in reached],
                    colorscale="Plasma",
                    cmin=0.0,
                    cmax=shared_vmax,
                    colorbar=dict(title=t("colorbar_arrival_time", lang)),
                    line=dict(width=1, color="white"),
                ),
                hovertext=[_node_hover_text(graph, n, lang, fire_times[n]) for n in reached],
                hoverinfo="text",
                showlegend=False,
            )
        )
    if unreached:
        traces.append(
            go.Scattergl(
                x=[pos[n][0] for n in unreached],
                y=[pos[n][1] for n in unreached],
                mode="markers+text",
                text=unreached,
                textposition="top center",
                textfont=dict(size=9),
                marker=dict(size=16, color="#cccccc", line=dict(width=1, color="white")),
                name=t("legend_not_reached", lang),
                hovertext=[_node_hover_text(graph, n, lang) for n in unreached],
                hoverinfo="text",
            )
        )
    return traces


def build_network_figure(
    graph: nx.DiGraph,
    fire_times: dict[str, float] | None = None,
    title: str = "",
    shared_vmax: float | None = None,
    lang: str = "en",
) -> go.Figure:
    """Interactive network figure.

    Colored by role if `fire_times` is None, otherwise colored by signal arrival
    time (nodes not yet reached shown in gray). Pass `shared_vmax` to keep the
    color scale consistent across a healthy/damaged pair of figures. `lang`
    controls hover/legend/colorbar text ("en" or "tr").
    """
    pos = layered_layout(graph)
    edge_traces = _edge_traces(graph, pos)
    node_traces = (
        _structure_node_traces(graph, pos, lang)
        if fire_times is None
        else _delay_node_traces(graph, fire_times, pos, shared_vmax, lang)
    )

    fig = go.Figure(data=edge_traces + node_traces)
    fig.update_layout(
        title=title,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor="white",
        height=550,
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    )
    return fig
