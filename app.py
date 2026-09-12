"""Interactive Mushroom Body signal-delay simulation.

Run with: streamlit run app.py
"""

import io as pyio
from pathlib import Path

import streamlit as st

from mbsim import io as mbio
from mbsim.calibration import ms_per_time_unit as default_ms_per_time_unit
from mbsim.damage import linear_slowdown, linear_threshold_increase
from mbsim.graph import build_graph, sanity_report
from mbsim.i18n import t
from mbsim.metrics import compare
from mbsim.mushroom_body import extract_mb_subgraph
from mbsim.perception import time_perception_deviation
from mbsim.perturbations import PERTURBATION_TYPES, per_edge_velocity_severity, per_node_threshold_severity
from mbsim.plotly_viz import (
    build_delay_delta_figure,
    build_network_figure,
    build_propagation_animation,
    build_weber_fechner_figure,
)
from mbsim.trials import compare_trials
from mbsim.validation import (
    compare_to_simulation,
    example_climbing_assay,
    example_time_perception_task,
    load_climbing_assay,
    load_time_perception_task,
)

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
def build_mb_graph(connections, classification, roles_key, extra_node_ids_key=()):
    roles = {role: list(cell_types) for role, cell_types in roles_key}
    edge_df, node_roles = extract_mb_subgraph(
        connections, classification, roles, extra_node_ids=list(extra_node_ids_key)
    )
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


def _sync_intensity(source_key, target_key):
    """Keep a perturbation's slider and number-input widgets showing the same value."""
    st.session_state[target_key] = st.session_state[source_key]


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

    st.header(t("header_perturbations", lang))
    if "perturbations" not in st.session_state:
        st.session_state.perturbations = []
    if "next_perturbation_id" not in st.session_state:
        st.session_state.next_perturbation_id = 0

    if st.button(t("btn_add_perturbation", lang), use_container_width=True):
        st.session_state.perturbations.append(
            {"id": st.session_state.next_perturbation_id, "type": "tau", "intensity": 0.0}
        )
        st.session_state.next_perturbation_id += 1

    if not st.session_state.perturbations:
        st.caption(t("msg_no_perturbations", lang))

    perturbation_type_options = list(PERTURBATION_TYPES.keys())
    remove_id = None
    for entry in st.session_state.perturbations:
        pid = entry["id"]
        slider_key, number_key = f"pert_slider_{pid}", f"pert_number_{pid}"
        st.session_state.setdefault(slider_key, entry["intensity"])
        st.session_state.setdefault(number_key, entry["intensity"])

        with st.container(border=True):
            type_col, remove_col = st.columns([5, 1])
            with type_col:
                entry["type"] = st.selectbox(
                    t("label_perturbation_type", lang),
                    perturbation_type_options,
                    index=perturbation_type_options.index(entry["type"]),
                    format_func=lambda key: t(PERTURBATION_TYPES[key]["label_key"], lang),
                    key=f"pert_type_{pid}",
                    help=t(PERTURBATION_TYPES[entry["type"]]["description_key"], lang),
                )
                if entry["type"] != "apl":
                    # Otherwise a root_id entered while this row was set to APL
                    # would silently survive the switch and narrow the new
                    # type's (e.g. Tau's normally-all-edges) target set down to
                    # that one neuron's outgoing edges.
                    entry.pop("target_root_ids", None)
            with remove_col:
                st.write("")
                if st.button(t("btn_remove_perturbation", lang), key=f"pert_remove_{pid}"):
                    remove_id = pid

            # Shown directly (not just as a hover tooltip on the selectbox above) so
            # what each factor represents is visible at a glance, not just on hover.
            st.caption(t(PERTURBATION_TYPES[entry["type"]]["description_key"], lang))

            slider_col, number_col = st.columns([3, 1])
            with slider_col:
                st.slider(
                    t("label_intensity", lang),
                    min_value=0.0,
                    max_value=100.0,
                    step=1.0,
                    key=slider_key,
                    on_change=_sync_intensity,
                    args=(slider_key, number_key),
                )
            with number_col:
                st.number_input(
                    t("label_intensity", lang),
                    min_value=0.0,
                    max_value=100.0,
                    step=1.0,
                    key=number_key,
                    on_change=_sync_intensity,
                    args=(number_key, slider_key),
                    label_visibility="collapsed",
                )
            entry["intensity"] = st.session_state[slider_key]

            if entry["type"] == "apl":
                root_ids_str = st.text_input(
                    t("label_apl_root_ids", lang),
                    value=",".join(entry.get("target_root_ids", [])),
                    key=f"pert_root_ids_{pid}",
                    help=t("help_apl_root_ids", lang),
                )
                entry["target_root_ids"] = [rid.strip() for rid in root_ids_str.split(",") if rid.strip()]

    if remove_id is not None:
        st.session_state.perturbations = [e for e in st.session_state.perturbations if e["id"] != remove_id]
        st.rerun()

    # Every perturbation's target_root_ids (currently only APL uses this) must be
    # force-included in the extracted subgraph below, or targeting.resolve_targets
    # would never see that neuron's edges at all — see mushroom_body.py's
    # extra_node_ids parameter.
    extra_node_ids = sorted(
        {rid for entry in st.session_state.perturbations for rid in entry.get("target_root_ids", [])}
    )

    with st.expander(t("header_calibration", lang)):
        st.caption(t("caption_calibration_source", lang))
        ms_per_time_unit = st.number_input(
            t("label_ms_calibration", lang),
            min_value=0.1,
            max_value=1000.0,
            value=default_ms_per_time_unit(),
            step=0.1,
        )

if not input_types or not relay_types or not output_types:
    st.warning(t("warn_select_roles", lang))
    st.stop()

roles_key = tuple(
    (role, tuple(sorted(types)))
    for role, types in [("input", input_types), ("relay", relay_types), ("output", output_types)]
)

try:
    graph, report, node_roles = build_mb_graph(connections, classification, roles_key, tuple(extra_node_ids))
except Exception as exc:
    st.error(t("err_build_graph", lang, error=exc))
    st.stop()

input_nodes = [n for n, r in node_roles.items() if r == "input" and n in graph]
output_nodes = [n for n, r in node_roles.items() if r == "output" and n in graph]

if not input_nodes or not output_nodes:
    st.warning(t("warn_no_input_output", lang))
    st.stop()

perturbations = st.session_state.perturbations
result = compare(
    graph,
    input_nodes,
    output_nodes,
    base_conduction_velocity=conduction_velocity,
    threshold=threshold,
    perturbations=perturbations,
    slowdown_fn=linear_slowdown,
    threshold_fn=linear_threshold_increase,
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

edge_severity = per_edge_velocity_severity(graph, perturbations)
node_severity = per_node_threshold_severity(graph, perturbations)
mean_edge_severity = sum(edge_severity.values()) / len(edge_severity) if edge_severity else 0.0
mean_node_severity = sum(node_severity.values()) / len(node_severity) if node_severity else 0.0

st.caption(
    t(
        "caption_velocity_severity",
        lang,
        n_targeted=len(edge_severity),
        n_total=report["n_edges"],
        pct=f"{mean_edge_severity * 100:.1f}",
    )
)
st.caption(
    t(
        "caption_threshold_severity",
        lang,
        n_targeted=len(node_severity),
        n_total=report["n_nodes"],
        pct=f"{mean_node_severity * 100:.1f}",
    )
)
if (max(edge_severity.values(), default=0.0)) >= 0.95 or (max(node_severity.values(), default=0.0)) >= 0.95:
    st.warning(t("warn_high_severity", lang))

tab_perception, tab_network, tab_comparison, tab_data, tab_propagation, tab_validation = st.tabs(
    [
        t("tab_perception", lang),
        t("tab_network", lang),
        t("tab_comparison", lang),
        t("tab_data", lang),
        t("tab_propagation", lang),
        t("tab_validation", lang),
    ]
)

with tab_perception:
    healthy_delays = [result.healthy_fire_times[n] for n in output_nodes if n in result.healthy_fire_times]
    damaged_delays = [result.damaged_fire_times[n] for n in output_nodes if n in result.damaged_fire_times]

    if not healthy_delays or not damaged_delays:
        st.warning(t("warn_signal_not_reached", lang))
    else:
        healthy_ms = (sum(healthy_delays) / len(healthy_delays)) * ms_per_time_unit
        damaged_ms = (sum(damaged_delays) / len(damaged_delays)) * ms_per_time_unit
        net_ms = damaged_ms - healthy_ms

        delay_col, wf_col = st.columns(2)
        with delay_col:
            st.subheader(t("header_physical_delay", lang))
            m1, m2, m3 = st.columns(3)
            m1.metric(t("metric_healthy_delay_ms", lang), f"{healthy_ms:.2f}")
            m2.metric(t("metric_damaged_delay_ms", lang), f"{damaged_ms:.2f}")
            m3.metric(t("metric_net_delay_ms", lang), f"{net_ms:+.2f}")

        with wf_col:
            st.subheader(t("header_weber_fechner", lang))
            st.caption(t("caption_weber_fechner", lang))
            perception = time_perception_deviation(healthy_ms, damaged_ms)
            st.plotly_chart(
                build_weber_fechner_figure(
                    perception["t"],
                    perception["healthy"],
                    perception["damaged"],
                    perception["pct_deviation"],
                    lang,
                ),
                use_container_width=True,
            )
            st.metric(t("metric_deviation_pct", lang), f"{perception['pct_deviation']:.1f}%")

        if not edge_severity and not node_severity:
            st.info(t("info_zero_severity", lang))

    with st.expander(t("header_trials", lang)):
        st.caption(t("caption_trials", lang))
        tcol1, tcol2, tcol3 = st.columns([1, 1, 1])
        with tcol1:
            n_trials = st.number_input(t("label_n_trials", lang), min_value=5, max_value=200, value=30, step=5)
        with tcol2:
            noise_std = st.slider(t("label_noise_std", lang), 0.0, 0.5, 0.1, 0.01)
        with tcol3:
            st.write("")
            run_clicked = st.button(t("btn_run_trials", lang))

        if run_clicked:
            with st.spinner(t("spinner_running_trials", lang)):
                st.session_state["trials_result"] = compare_trials(
                    graph,
                    input_nodes,
                    output_nodes,
                    base_conduction_velocity=conduction_velocity,
                    threshold=threshold,
                    perturbations=perturbations,
                    n_trials=int(n_trials),
                    noise_std=noise_std,
                    slowdown_fn=linear_slowdown,
                    threshold_fn=linear_threshold_increase,
                    seed=0,
                )

        trials_result = st.session_state.get("trials_result")
        if trials_result is not None:
            hwf, dwf = trials_result["healthy_weber_fraction"], trials_result["damaged_weber_fraction"]
            wcol1, wcol2 = st.columns(2)
            wcol1.metric(
                t("metric_healthy_weber_fraction", lang), f"{hwf * 100:.1f}%" if hwf is not None else "n/a"
            )
            wcol2.metric(
                t("metric_damaged_weber_fraction", lang), f"{dwf * 100:.1f}%" if dwf is not None else "n/a"
            )
        else:
            st.caption(t("caption_trials_not_run", lang))

with tab_network:
    if result.df.empty:
        st.warning(t("warn_signal_not_reached", lang))
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric(
        t("metric_mean_dev", lang),
        f"{result.summary['mean_pct_deviation']:.1f}%" if result.summary["mean_pct_deviation"] is not None else "n/a",
    )
    col2.metric(
        t("metric_median_dev", lang),
        f"{result.summary['median_pct_deviation']:.1f}%" if result.summary["median_pct_deviation"] is not None else "n/a",
    )
    mean_velocity = result.summary["mean_targeted_damaged_velocity"]
    col3.metric(
        t("metric_damaged_velocity", lang),
        f"{mean_velocity:.3f}" if mean_velocity is not None else "n/a",
    )
    mean_threshold = result.summary["mean_targeted_damaged_threshold"]
    col4.metric(
        t("metric_damaged_threshold", lang),
        f"{mean_threshold:.3f}" if mean_threshold is not None else "n/a",
    )
    col5.metric(
        t("metric_outputs_reached", lang),
        f"{result.summary['n_output_nodes_reached']}/{result.summary['n_output_nodes_total']}",
    )

    st.caption(t("caption_delta_chart", lang))
    st.plotly_chart(
        build_delay_delta_figure(
            graph, result.healthy_fire_times, result.damaged_fire_times, t("chart_delta_title", lang), lang
        ),
        use_container_width=True,
    )

    with st.expander(t("expander_absolute_times", lang)):
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
    column_labels = {
        "node": t("col_node", lang),
        "healthy_time": t("col_healthy_time", lang),
        "damaged_time": t("col_damaged_time", lang),
        "pct_deviation": t("col_pct_deviation", lang),
    }
    st.dataframe(result.df.rename(columns=column_labels), use_container_width=True)
    st.download_button(
        t("download_button", lang),
        result.df.to_csv(index=False),
        file_name="comparison.csv",
        mime="text/csv",
    )

with tab_propagation:
    st.caption(t("caption_propagation", lang))
    speed_ms = st.slider(t("label_anim_speed", lang), 50, 1500, 400, 50)
    st.plotly_chart(
        build_propagation_animation(
            graph, result.healthy_fire_times, result.damaged_fire_times, lang, frame_duration_ms=speed_ms
        ),
        use_container_width=True,
    )

with tab_validation:
    st.caption(t("caption_validation", lang))

    climbing_upload, clinical_upload = st.columns(2)
    with climbing_upload:
        climbing_file = st.file_uploader(
            t("label_climbing_upload", lang), type="csv", help=t("help_climbing_upload", lang)
        )
    with clinical_upload:
        clinical_file = st.file_uploader(
            t("label_clinical_upload", lang), type="csv", help=t("help_clinical_upload", lang)
        )

    if "use_example_validation" not in st.session_state:
        st.session_state.use_example_validation = False
    if st.button(t("btn_load_example_validation", lang)):
        st.session_state.use_example_validation = True

    climbing_df = clinical_df = None
    validation_error = None
    try:
        if climbing_file is not None:
            climbing_df = load_climbing_assay(pyio.BytesIO(climbing_file.getvalue()))
        elif st.session_state.use_example_validation:
            climbing_df = example_climbing_assay()

        if clinical_file is not None:
            clinical_df = load_time_perception_task(pyio.BytesIO(clinical_file.getvalue()))
        elif st.session_state.use_example_validation:
            clinical_df = example_time_perception_task()
    except Exception as exc:
        validation_error = exc

    if validation_error is not None:
        st.error(t("err_validation_load", lang, error=validation_error))
    elif climbing_df is None and clinical_df is None:
        st.info(t("info_no_validation_data", lang))
    else:
        if climbing_file is None and clinical_file is None and st.session_state.use_example_validation:
            st.caption(t("caption_example_validation", lang))

        sim_pct_deviation = result.summary["mean_pct_deviation"]
        if sim_pct_deviation is None:
            st.warning(t("warn_validation_no_sim_deviation", lang))
        else:
            validation_result = compare_to_simulation(
                sim_pct_deviation, climbing_df=climbing_df, clinical_df=clinical_df
            )

            vcol1, vcol2, vcol3 = st.columns(3)
            vcol1.metric(t("metric_sim_deviation", lang), f"{validation_result['simulation_pct_deviation']:.1f}%")

            if "fly_pct_deviation" in validation_result:
                vcol2.metric(t("metric_fly_deviation", lang), f"{validation_result['fly_pct_deviation']:.1f}%")
                same = validation_result["fly_same_direction_as_simulation"]
                vcol2.caption(
                    f"{t('label_same_direction', lang)} "
                    f"{t('same_direction_yes', lang) if same else t('same_direction_no', lang)}"
                )

            if "human_excess_pct_deviation" in validation_result:
                vcol3.metric(
                    t("metric_human_deviation", lang), f"{validation_result['human_excess_pct_deviation']:.1f}%"
                )
                same = validation_result["human_same_direction_as_simulation"]
                vcol3.caption(
                    f"{t('label_same_direction', lang)} "
                    f"{t('same_direction_yes', lang) if same else t('same_direction_no', lang)}"
                )
