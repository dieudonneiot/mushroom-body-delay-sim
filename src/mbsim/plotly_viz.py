"""Interactive Plotly renderings of the Mushroom Body graph, for the Streamlit UI.

Uses the same layered layout / role colors as the static matplotlib report in
visualize.py, but adds hover tooltips, zoom/pan, and an animated playback view.
"""

from collections import defaultdict

import networkx as nx
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from mbsim.i18n import t
from mbsim.layout import (
    DEFAULT_ROLE_COLOR,
    ROLE_COLORS,
    edge_style,
    layered_layout,
    marker_size,
    show_node_labels,
)

N_EDGE_WIDTH_BUCKETS = 5
N_ANIMATION_FRAMES = 40


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
    min_width, max_width, alpha = edge_style(len(weights))

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
        width = min_width + (max_width - min_width) * (bucket / max(N_EDGE_WIDTH_BUCKETS - 1, 1))
        traces.append(
            go.Scattergl(
                x=xs,
                y=ys,
                mode="lines",
                line=dict(width=width, color=f"rgba(120,120,120,{alpha})"),
                hoverinfo="skip",
                showlegend=False,
            )
        )
    return traces


def _structure_node_traces(graph: nx.DiGraph, pos: dict, lang: str) -> list[go.Scattergl]:
    size = marker_size(graph.number_of_nodes())
    show_text = show_node_labels(graph.number_of_nodes())
    roles = sorted({data.get("role") for _, data in graph.nodes(data=True)})
    traces = []
    for role in roles:
        nodes = [n for n, d in graph.nodes(data=True) if d.get("role") == role]
        traces.append(
            go.Scattergl(
                x=[pos[n][0] for n in nodes],
                y=[pos[n][1] for n in nodes],
                mode="markers+text" if show_text else "markers",
                text=nodes,
                textposition="top center",
                textfont=dict(size=9),
                marker=dict(
                    size=size,
                    color=ROLE_COLORS.get(role, DEFAULT_ROLE_COLOR),
                    line=dict(width=1 if show_text else 0.3, color="white"),
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
    size = marker_size(graph.number_of_nodes())
    show_text = show_node_labels(graph.number_of_nodes())
    reached = [n for n in graph.nodes if n in fire_times]
    unreached = [n for n in graph.nodes if n not in fire_times]
    shared_vmax = vmax if vmax is not None else (max(fire_times.values()) if fire_times else 1.0)

    traces = []
    if reached:
        traces.append(
            go.Scattergl(
                x=[pos[n][0] for n in reached],
                y=[pos[n][1] for n in reached],
                mode="markers+text" if show_text else "markers",
                text=reached,
                textposition="top center",
                textfont=dict(size=9),
                marker=dict(
                    size=size,
                    color=[fire_times[n] for n in reached],
                    colorscale="Plasma",
                    cmin=0.0,
                    cmax=shared_vmax,
                    colorbar=dict(title=t("colorbar_arrival_time", lang)),
                    line=dict(width=1 if show_text else 0.3, color="white"),
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
                mode="markers+text" if show_text else "markers",
                text=unreached,
                textposition="top center",
                textfont=dict(size=9),
                marker=dict(size=size, color="#cccccc", line=dict(width=1 if show_text else 0.3, color="white")),
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
    controls hover/legend/colorbar text ("en" or "tr"). Marker size, labels, and
    edge opacity all scale down automatically for large (real-connectome-sized)
    graphs — see mbsim.layout.marker_size/show_node_labels/edge_style.
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


_ROLE_ORDER = ("input", "relay", "output")


def _nodes_by_role(graph: nx.DiGraph) -> dict[str, list[str]]:
    buckets: dict[str, list[str]] = {role: [] for role in _ROLE_ORDER}
    for node, data in graph.nodes(data=True):
        role = data.get("role")
        if role in buckets:
            buckets[role].append(node)
    return buckets


def _propagation_frame_traces(
    nodes_by_role: dict[str, list[str]],
    pos: dict,
    fire_times: dict[str, float],
    tau: float,
    size: float,
) -> list[dict]:
    """One flat-colored trace per role for active (fired-by-tau) nodes, plus one shared
    gray trace for everything not yet active. Using a single scalar color per trace
    (instead of a per-node color array) avoids Plotly's per-element color validation,
    which otherwise dominates build time on graphs with thousands of nodes."""
    traces = []
    inactive_x: list[float] = []
    inactive_y: list[float] = []
    for role in _ROLE_ORDER:
        active_x: list[float] = []
        active_y: list[float] = []
        for node in nodes_by_role[role]:
            fire_time = fire_times.get(node)
            x, y = pos[node]
            if fire_time is not None and fire_time <= tau:
                active_x.append(x)
                active_y.append(y)
            else:
                inactive_x.append(x)
                inactive_y.append(y)
        traces.append(
            dict(
                type="scattergl",
                x=active_x,
                y=active_y,
                mode="markers",
                marker=dict(size=size, color=ROLE_COLORS[role], line=dict(width=0.3, color="white")),
                hoverinfo="skip",
                showlegend=False,
            )
        )
    traces.append(
        dict(
            type="scattergl",
            x=inactive_x,
            y=inactive_y,
            mode="markers",
            marker=dict(size=size, color="#e2e2e2"),
            hoverinfo="skip",
            showlegend=False,
        )
    )
    return traces


def _propagation_status_text(lang: str, tau: float, h_count: int, d_count: int, total: int) -> str:
    return (
        f"t = {tau:.3f}   |   {t('anim_fired_healthy', lang)}: {h_count}/{total}"
        f"   |   {t('anim_fired_damaged', lang)}: {d_count}/{total}"
    )


def build_propagation_animation(
    graph: nx.DiGraph,
    healthy_fire_times: dict[str, float],
    damaged_fire_times: dict[str, float],
    lang: str = "en",
    frame_duration_ms: int = 300,
    n_frames: int = N_ANIMATION_FRAMES,
) -> go.Figure:
    """Side-by-side animated playback of the signal spreading through the healthy vs.
    damaged network on a shared simulated-time axis, so the damaged network's lag is
    directly visible while it plays. Nodes light up (role-colored) the instant they
    fire; a running "t = ... / fired X/Y" readout above the charts makes the lag
    legible as numbers, not just as a subtle visual difference. Edges are omitted here
    — at real-connectome scale they'd dominate the frame and this view is about the
    wavefront of activation, not connectivity detail (use `build_network_figure`'s
    static, hoverable view for that). `frame_duration_ms` controls playback speed —
    higher is slower, for a clearer look at what's happening moment to moment.
    """
    pos = layered_layout(graph)
    size = marker_size(graph.number_of_nodes())
    nodes_by_role = _nodes_by_role(graph)
    total_nodes = graph.number_of_nodes()

    all_times = sorted(list(healthy_fire_times.values()) + list(damaged_fire_times.values()))
    if len(all_times) >= 2 and n_frames > 1:
        # Quantile-spaced frames, not linear-in-time: fire times are heavily front-loaded
        # (most of the network fires almost immediately, then a long tail of stragglers),
        # so linear spacing wastes nearly all frames on that tail. Spacing by quantile
        # instead means each frame reveals a similar number of newly-active nodes —
        # a smooth, evenly-paced wave instead of one flash followed by a long dribble.
        frame_taus = [
            all_times[round(q * (len(all_times) - 1))] for q in (i / (n_frames - 1) for i in range(n_frames))
        ]
    else:
        frame_taus = [all_times[0]] if all_times else [0.0]

    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=[t("chart_healthy_network", lang), t("chart_damaged_network", lang)],
    )

    for trace in _propagation_frame_traces(nodes_by_role, pos, healthy_fire_times, frame_taus[0], size):
        fig.add_trace(trace, row=1, col=1)
    for trace in _propagation_frame_traces(nodes_by_role, pos, damaged_fire_times, frame_taus[0], size):
        fig.add_trace(trace, row=1, col=2)

    frames = []
    initial_title = None
    for i, tau in enumerate(frame_taus):
        h_traces = _propagation_frame_traces(nodes_by_role, pos, healthy_fire_times, tau, size)
        d_traces = _propagation_frame_traces(nodes_by_role, pos, damaged_fire_times, tau, size)
        h_count = sum(len(tr["x"]) for tr in h_traces[:3])
        d_count = sum(len(tr["x"]) for tr in d_traces[:3])
        status_text = _propagation_status_text(lang, tau, h_count, d_count, total_nodes)
        if i == 0:
            initial_title = status_text
        # The running "t=... fired X/Y" readout lives in the figure title (a single
        # scalar property), not in `layout.annotations` (an array) — per-frame array
        # updates left ghost text from the previous frame overlapping the new one.
        frames.append(
            go.Frame(
                data=h_traces + d_traces,
                name=f"{tau:.4f}",
                layout=go.Layout(title=dict(text=status_text)),
            )
        )
    fig.frames = frames

    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    # Visible divider between the two panels, so it reads unambiguously as two
    # separate networks side by side rather than one merged chart.
    fig.add_shape(
        type="line",
        xref="paper",
        yref="paper",
        x0=0.5,
        x1=0.5,
        y0=0.0,
        y1=1.0,
        line=dict(color="rgba(140,140,140,0.7)", width=2, dash="solid"),
    )
    fig.update_layout(
        height=550,
        margin=dict(l=10, r=10, t=90, b=10),
        showlegend=False,
        title=dict(text=initial_title or "", x=0.5, xanchor="center", font=dict(size=15)),
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                x=0.0,
                y=1.3,
                xanchor="left",
                yanchor="top",
                buttons=[
                    dict(
                        label=t("anim_play", lang),
                        method="animate",
                        args=[
                            None,
                            dict(
                                frame=dict(duration=frame_duration_ms, redraw=True),
                                fromcurrent=True,
                                transition=dict(duration=0),
                            ),
                        ],
                    ),
                    dict(
                        label=t("anim_pause", lang),
                        method="animate",
                        args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate", transition=dict(duration=0))],
                    ),
                ],
            )
        ],
        sliders=[
            dict(
                active=0,
                x=0.1,
                len=0.85,
                currentvalue=dict(prefix=f"{t('anim_time_prefix', lang)}: "),
                steps=[
                    dict(
                        method="animate",
                        label=f"{tau:.3f}",
                        args=[[f"{tau:.4f}"], dict(mode="immediate", frame=dict(duration=0, redraw=True), transition=dict(duration=0))],
                    )
                    for tau in frame_taus
                ],
            )
        ],
    )
    return fig
