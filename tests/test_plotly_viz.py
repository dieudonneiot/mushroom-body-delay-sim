from pathlib import Path

import networkx as nx
import plotly.graph_objects as go

from mbsim.graph import build_graph
from mbsim.io import load_raw_data
from mbsim.metrics import compare
from mbsim.mushroom_body import extract_mb_subgraph
from mbsim.plotly_viz import build_delay_delta_figure, build_network_figure, build_propagation_animation

FIXTURE_DIR = Path(__file__).parent.parent / "data" / "fixtures"
ROLES = {"input": ["PN"], "relay": ["KC"], "output": ["MBON"]}


def _fixture_graph():
    connections, classification = load_raw_data(FIXTURE_DIR)
    edge_df, node_roles = extract_mb_subgraph(connections, classification, ROLES)
    return build_graph(edge_df, node_roles)


def test_structure_figure_has_one_trace_per_role():
    graph = _fixture_graph()
    fig = build_network_figure(graph, fire_times=None, title="structure")

    assert isinstance(fig, go.Figure)
    node_trace_names = {t.name for t in fig.data if t.mode and "markers" in t.mode}
    assert node_trace_names == {"input", "relay", "output"}


def test_delay_figure_colors_reached_nodes():
    graph = _fixture_graph()
    result = compare(graph, ["PN1", "PN2", "PN3"], ["MBON1", "MBON2"])
    fig = build_network_figure(graph, fire_times=result.healthy_fire_times, title="delay")

    assert isinstance(fig, go.Figure)
    marker_traces = [t for t in fig.data if t.mode and "markers" in t.mode]
    all_nodes = {n for t in marker_traces for n in t.text}
    assert all_nodes == set(graph.nodes)


def test_delay_figure_shows_unreached_nodes_separately():
    graph = _fixture_graph()
    partial_fire_times = {"PN1": 0.0, "PN2": 0.0, "PN3": 0.0}
    fig = build_network_figure(graph, fire_times=partial_fire_times, title="partial")

    unreached_traces = [t for t in fig.data if t.name == "not reached"]
    assert len(unreached_traces) == 1
    assert set(unreached_traces[0].text) == set(graph.nodes) - {"PN1", "PN2", "PN3"}


def test_delta_figure_colors_by_damaged_minus_healthy():
    graph = _fixture_graph()
    healthy = {"PN1": 0.0, "KC1": 1.0, "MBON1": 2.0}
    damaged = {"PN1": 0.0, "KC1": 1.0, "MBON1": 3.0}  # only MBON1 got slower
    fig = build_delay_delta_figure(graph, healthy, damaged, title="delta")

    marker_trace = next(t for t in fig.data if t.mode and "markers" in t.mode and t.text)
    deltas = dict(zip(marker_trace.text, marker_trace.marker.color))
    assert deltas["MBON1"] == 1.0
    assert deltas["PN1"] == 0.0
    assert deltas["KC1"] == 0.0
    # Diverging scale centered at zero, sized to the actual spread (1.0), not
    # to some unrelated absolute arrival time.
    assert marker_trace.marker.cmin == -1.0
    assert marker_trace.marker.cmax == 1.0


def test_delta_figure_separates_nodes_missing_from_either_side():
    graph = _fixture_graph()
    healthy = {"PN1": 0.0, "KC1": 1.0}  # MBON1 never reached healthy
    damaged = {"PN1": 0.0, "KC1": 1.0, "MBON1": 3.0}
    fig = build_delay_delta_figure(graph, healthy, damaged, title="delta")

    unreached_traces = [t for t in fig.data if t.name == "not reached"]
    assert len(unreached_traces) == 1
    assert "MBON1" in unreached_traces[0].text


def _graph_with_modulatory_node():
    graph = nx.DiGraph()
    graph.add_node("A", role="input")
    graph.add_node("B", role="relay")
    graph.add_node("C", role="output")
    graph.add_node("D", role="modulatory")  # e.g. a manually-targeted APL neuron
    graph.add_edge("A", "B", weight=1)
    graph.add_edge("B", "C", weight=1)
    graph.add_edge("A", "D", weight=1)
    return graph


def test_propagation_animation_includes_modulatory_node_once_fired():
    """Regression test: a manually force-included modulatory neuron (e.g. APL,
    via mushroom_body.extract_mb_subgraph's extra_node_ids) must actually appear
    in the Live Propagation animation and count toward the fired total, not be
    silently dropped because _ROLE_ORDER only listed input/relay/output."""
    graph = _graph_with_modulatory_node()
    fire_times = {"A": 0.0, "B": 0.1, "C": 0.2, "D": 0.15}

    fig = build_propagation_animation(graph, fire_times, fire_times, n_frames=2)

    last_frame = fig.frames[-1]
    # 5 traces per subplot (input/relay/output/modulatory active + 1 shared
    # inactive), 2 subplots (healthy, damaged) = 10.
    assert len(last_frame.data) == 10
    all_plotted_points = sum(len(tr["x"]) for tr in last_frame.data)
    assert all_plotted_points == 8  # 4 nodes x 2 subplots, all fired by the last frame

    assert "fired: 4/4" in last_frame.layout.title.text
