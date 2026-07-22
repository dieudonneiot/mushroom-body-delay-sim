from pathlib import Path

import plotly.graph_objects as go

from mbsim.graph import build_graph
from mbsim.io import load_raw_data
from mbsim.metrics import compare
from mbsim.mushroom_body import extract_mb_subgraph
from mbsim.plotly_viz import build_network_figure

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
