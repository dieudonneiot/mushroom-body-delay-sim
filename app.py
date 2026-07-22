"""Interactive Mushroom Body signal-delay simulation.

Run with: streamlit run app.py
"""

import io as pyio
from pathlib import Path

import streamlit as st

from mbsim import io as mbio
from mbsim.damage import linear_slowdown
from mbsim.graph import build_graph, sanity_report
from mbsim.i18n import t
from mbsim.metrics import compare
from mbsim.mushroom_body import extract_mb_subgraph
from mbsim.plotly_viz import build_network_figure

st.set_page_config(page_title="Mushroom Body Delay Simulator", page_icon="🧠", layout="wide")

FIXTURE_DIR = Path("data/fixtures")
RAW_DIR = Path("data/raw")
DEFAULT_ROLE_GUESSES = {
    "input": ["PN", "ALPN"],
    "relay": ["KC", "Kenyon_Cell"],
    "output": ["MBON"],
}


@st.cache_data(show_spinner="Loading connectome data...")
def load_connectome(data_mode, connections_bytes, classification_bytes):
    if data_mode == "upload":
        connections = mbio.load_connections(pyio.BytesIO(connections_bytes))
        classification = mbio.load_classification(pyio.BytesIO(classification_bytes))
    else:
        data_dir = FIXTURE_DIR if data_mode == "fixture" else RAW_DIR
        connections, classification = mbio.load_raw_data(data_dir)
    return connections, classification


@st.cache_data(show_spinner="Building Mushroom Body graph...")
def build_mb_graph(connections, classification, roles_key):
    roles = {role: list(cell_types) for role, cell_types in roles_key}
    edge_df, node_roles = extract_mb_subgraph(connections, classification, roles)
    graph = build_graph(edge_df, node_roles)
    report = sanity_report(graph)
    return graph, report, node_roles


def default_selection(cell_types, role):
    for guess in DEFAULT_ROLE_GUESSES[role]:
        if guess in cell_types:
            return [guess]
    return []


def format_role_counts(role_counts: dict, lang: str) -> str:
    return ", ".join(f"{t(f'role_{role}', lang)}: {count}" for role, count in role_counts.items())


# --- Language toggle (first, so everything below can be translated) ---
with st.sidebar:
    lang_label = st.radio(t("language_label", "en"), ["English", "Türkçe"], horizontal=True)
    lang = {"English": "en", "Türkçe": "tr"}[lang_label]
    st.divider()

st.title(t("app_title", lang))
st.caption(t("app_caption", lang))

with st.sidebar:
    st.header(t("header_data_source", lang))
    data_mode_options = [t("opt_fixture", lang), t("opt_raw", lang), t("opt_upload", lang)]
    data_mode_label = st.radio(t("label_data_source_radio", lang), data_mode_options, index=0)
    data_mode = dict(zip(data_mode_options, ["fixture", "raw", "upload"]))[data_mode_label]

    connections_bytes = classification_bytes = None
    if data_mode == "upload":
        connections_file = st.file_uploader(
            "connections.csv", type="csv", help=t("uploader_connections_help", lang)
        )
        classification_file = st.file_uploader(
            "classification.csv", type="csv", help=t("uploader_classification_help", lang)
        )
        if connections_file and classification_file:
            connections_bytes = connections_file.getvalue()
            classification_bytes = classification_file.getvalue()

    ready = data_mode != "upload" or (connections_bytes and classification_bytes)
    if not ready:
        st.info(t("msg_upload_both", lang))
        st.stop()

    if data_mode == "raw" and not (RAW_DIR / "connections.csv").exists():
        st.error(t("err_raw_missing", lang))
        st.stop()

    try:
        connections, classification = load_connectome(data_mode, connections_bytes, classification_bytes)
    except Exception as exc:
        st.error(t("err_load_data", lang, error=exc))
        st.stop()

    all_cell_types = sorted(classification["cell_type"].dropna().unique().tolist())

    st.header(t("header_pathway", lang))
    input_types = st.multiselect(
        t("label_input_types", lang), all_cell_types, default=default_selection(all_cell_types, "input")
    )
    relay_types = st.multiselect(
        t("label_relay_types", lang), all_cell_types, default=default_selection(all_cell_types, "relay")
    )
    output_types = st.multiselect(
        t("label_output_types", lang), all_cell_types, default=default_selection(all_cell_types, "output")
    )

    st.header(t("header_sim_params", lang))
    conduction_velocity = st.slider(t("label_conduction_velocity", lang), 0.1, 3.0, 1.0, 0.1)
    threshold = st.slider(t("label_threshold", lang), 0.5, 5.0, 1.0, 0.1)
    severity = st.slider(t("label_severity", lang), 0.0, 1.0, 0.3, 0.01)

if not input_types or not relay_types or not output_types:
    st.warning(t("warn_select_roles", lang))
    st.stop()

roles_key = tuple(
    (role, tuple(sorted(types)))
    for role, types in [("input", input_types), ("relay", relay_types), ("output", output_types)]
)

try:
    graph, report, node_roles = build_mb_graph(connections, classification, roles_key)
except Exception as exc:
    st.error(t("err_build_graph", lang, error=exc))
    st.stop()

input_nodes = [n for n, r in node_roles.items() if r == "input" and n in graph]
output_nodes = [n for n, r in node_roles.items() if r == "output" and n in graph]

if not input_nodes or not output_nodes:
    st.warning(t("warn_no_input_output", lang))
    st.stop()

result = compare(
    graph,
    input_nodes,
    output_nodes,
    base_conduction_velocity=conduction_velocity,
    threshold=threshold,
    severity=severity,
    slowdown_fn=linear_slowdown,
)

st.caption(
    t(
        "caption_graph_stats",
        lang,
        n_nodes=report["n_nodes"],
        n_edges=report["n_edges"],
        role_counts=format_role_counts(report["role_counts"], lang),
    )
)

tab_network, tab_comparison, tab_data = st.tabs(
    [t("tab_network", lang), t("tab_comparison", lang), t("tab_data", lang)]
)

with tab_network:
    if result.df.empty:
        st.warning(t("warn_signal_not_reached", lang))
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        t("metric_mean_dev", lang),
        f"{result.summary['mean_pct_deviation']:.1f}%" if result.summary["mean_pct_deviation"] is not None else "n/a",
    )
    col2.metric(
        t("metric_median_dev", lang),
        f"{result.summary['median_pct_deviation']:.1f}%" if result.summary["median_pct_deviation"] is not None else "n/a",
    )
    col3.metric(t("metric_damaged_velocity", lang), f"{result.summary['damaged_conduction_velocity']:.3f}")
    col4.metric(
        t("metric_outputs_reached", lang),
        f"{result.summary['n_output_nodes_reached']}/{result.summary['n_output_nodes_total']}",
    )

    shared_vmax = max(
        max(result.healthy_fire_times.values(), default=0.0),
        max(result.damaged_fire_times.values(), default=0.0),
    )

    net_col1, net_col2 = st.columns(2)
    with net_col1:
        st.plotly_chart(
            build_network_figure(
                graph, result.healthy_fire_times, t("chart_healthy_network", lang), shared_vmax, lang
            ),
            use_container_width=True,
        )
    with net_col2:
        st.plotly_chart(
            build_network_figure(
                graph, result.damaged_fire_times, t("chart_damaged_network", lang), shared_vmax, lang
            ),
            use_container_width=True,
        )

    with st.expander(t("expander_structure", lang)):
        st.plotly_chart(
            build_network_figure(graph, None, t("chart_structure_title", lang), lang=lang),
            use_container_width=True,
        )

with tab_comparison:
    import plotly.graph_objects as go

    df = result.df
    if df.empty:
        st.warning(t("warn_no_compare", lang))
    else:
        fig = go.Figure()
        fig.add_bar(x=df["node"], y=df["healthy_time"], name=t("legend_healthy", lang))
        fig.add_bar(x=df["node"], y=df["damaged_time"], name=t("legend_damaged", lang))
        fig.update_layout(
            barmode="group",
            title=t("chart_bar_title", lang),
            yaxis_title=t("axis_arrival_time", lang),
            height=450,
        )
        st.plotly_chart(fig, use_container_width=True)

with tab_data:
    st.dataframe(result.df, use_container_width=True)
    st.download_button(
        t("download_button", lang),
        result.df.to_csv(index=False),
        file_name="comparison.csv",
        mime="text/csv",
    )
