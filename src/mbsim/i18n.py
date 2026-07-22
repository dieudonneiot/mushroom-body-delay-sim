"""UI string translations for the Streamlit app (English / Turkish)."""

STRINGS = {
    "app_title": {
        "en": "🧠 Mushroom Body Signal-Delay Simulator",
        "tr": "🧠 Mantar Cisimciği Sinyal Gecikmesi Simülatörü",
    },
    "app_caption": {
        "en": (
            "Simulating how Alzheimer's-driven slowing of neuronal conduction velocity "
            "delays signal transit through the Drosophila Mushroom Body (FlyWire/Codex connectome)."
        ),
        "tr": (
            "Alzheimer hastalığının neden olduğu nöral iletim hızı yavaşlamasının, meyve sineğinin "
            "(Drosophila) Mantar Cisimciği üzerinden sinyal iletimini nasıl geciktirdiğini simüle eder "
            "(FlyWire/Codex konektomu)."
        ),
    },
    "language_label": {"en": "🌐 Language / Dil", "tr": "🌐 Language / Dil"},
    "header_data_source": {"en": "Data source", "tr": "Veri kaynağı"},
    "label_data_source_radio": {"en": "Connectome data", "tr": "Konektom verisi"},
    "opt_fixture": {"en": "Fixture (demo data)", "tr": "Örnek veri (demo)"},
    "opt_raw": {"en": "data/raw/ (local files)", "tr": "data/raw/ (yerel dosyalar)"},
    "opt_upload": {"en": "Upload CSVs", "tr": "CSV yükle"},
    "uploader_connections_help": {
        "en": "The connections.csv export from Codex",
        "tr": "Codex'ten alınan connections.csv dosyası",
    },
    "uploader_classification_help": {
        "en": "The classification.csv export from Codex",
        "tr": "Codex'ten alınan classification.csv dosyası",
    },
    "msg_upload_both": {
        "en": "Upload both connections.csv and classification.csv to continue.",
        "tr": "Devam etmek için hem connections.csv hem de classification.csv dosyalarını yükleyin.",
    },
    "err_raw_missing": {
        "en": (
            "No data found in data/raw/. See data/raw/README.md for how to export it "
            "from codex.flywire.ai, or pick a different data source above."
        ),
        "tr": (
            "data/raw/ içinde veri bulunamadı. codex.flywire.ai'den nasıl dışa aktarılacağını "
            "öğrenmek için data/raw/README.md dosyasına bakın veya yukarıdan farklı bir veri "
            "kaynağı seçin."
        ),
    },
    "err_load_data": {
        "en": "Could not load data: {error}",
        "tr": "Veri yüklenemedi: {error}",
    },
    "header_pathway": {"en": "Mushroom Body pathway", "tr": "Mantar Cisimciği yolağı"},
    "label_input_types": {"en": "Input cell type(s)", "tr": "Girdi hücre tipi/tipleri"},
    "label_relay_types": {"en": "Relay cell type(s)", "tr": "Aktarıcı (relay) hücre tipi/tipleri"},
    "label_output_types": {"en": "Output cell type(s)", "tr": "Çıktı hücre tipi/tipleri"},
    "header_sim_params": {"en": "Simulation parameters", "tr": "Simülasyon parametreleri"},
    "label_conduction_velocity": {
        "en": "Healthy conduction velocity",
        "tr": "Sağlıklı iletim hızı",
    },
    "label_threshold": {"en": "Firing threshold", "tr": "Ateşleme eşiği"},
    "label_severity": {"en": "Disease severity", "tr": "Hastalık şiddeti"},
    "warn_select_roles": {
        "en": "Select at least one cell type for each of input, relay, and output.",
        "tr": "Girdi, aktarıcı ve çıktı için en az birer hücre tipi seçin.",
    },
    "err_build_graph": {
        "en": "Could not build the Mushroom Body graph: {error}",
        "tr": "Mantar Cisimciği grafiği oluşturulamadı: {error}",
    },
    "warn_no_input_output": {
        "en": "No input or output neurons found in the graph with the current role selection.",
        "tr": "Mevcut rol seçimiyle grafikte girdi veya çıktı nöronu bulunamadı.",
    },
    "caption_graph_stats": {
        "en": "Graph: {n_nodes} neurons, {n_edges} synaptic connections ({role_counts})",
        "tr": "Grafik: {n_nodes} nöron, {n_edges} sinaptik bağlantı ({role_counts})",
    },
    "tab_network": {"en": "Network View", "tr": "Ağ Görünümü"},
    "tab_comparison": {"en": "Comparison", "tr": "Karşılaştırma"},
    "tab_data": {"en": "Data", "tr": "Veri"},
    "warn_signal_not_reached": {
        "en": "The signal never reached an output neuron with the current role selection.",
        "tr": "Mevcut rol seçimiyle sinyal hiçbir çıktı nöronuna ulaşmadı.",
    },
    "metric_mean_dev": {"en": "Mean delay deviation", "tr": "Ortalama gecikme sapması"},
    "metric_median_dev": {"en": "Median delay deviation", "tr": "Medyan gecikme sapması"},
    "metric_damaged_velocity": {
        "en": "Damaged conduction velocity",
        "tr": "Hasarlı iletim hızı",
    },
    "metric_outputs_reached": {
        "en": "Output neurons reached",
        "tr": "Ulaşılan çıktı nöronu",
    },
    "chart_healthy_network": {"en": "Healthy network", "tr": "Sağlıklı ağ"},
    "chart_damaged_network": {"en": "Damaged network", "tr": "Hasarlı ağ"},
    "chart_structure_title": {"en": "Mushroom Body pathway", "tr": "Mantar Cisimciği yolağı"},
    "expander_structure": {
        "en": "Show pathway structure (colored by role)",
        "tr": "Yolak yapısını göster (role göre renklendirilmiş)",
    },
    "warn_no_compare": {
        "en": "No output neurons were reached by the signal — nothing to compare.",
        "tr": "Sinyal hiçbir çıktı nöronuna ulaşmadı — karşılaştırılacak bir şey yok.",
    },
    "chart_bar_title": {
        "en": "Signal arrival time at output neurons",
        "tr": "Çıktı nöronlarında sinyal varış zamanı",
    },
    "axis_arrival_time": {"en": "Arrival time", "tr": "Varış zamanı"},
    "legend_healthy": {"en": "Healthy", "tr": "Sağlıklı"},
    "legend_damaged": {"en": "Damaged", "tr": "Hasarlı"},
    "download_button": {"en": "Download comparison.csv", "tr": "comparison.csv dosyasını indir"},
    # plotly_viz.py hover / legend / colorbar strings
    "hover_id": {"en": "id", "tr": "kimlik"},
    "hover_role": {"en": "role", "tr": "rol"},
    "hover_in_degree": {"en": "in-degree", "tr": "gelen bağlantı"},
    "hover_out_degree": {"en": "out-degree", "tr": "giden bağlantı"},
    "hover_arrival_time": {"en": "arrival time", "tr": "varış zamanı"},
    "legend_not_reached": {"en": "not reached", "tr": "ulaşılamadı"},
    "colorbar_arrival_time": {"en": "Arrival time", "tr": "Varış zamanı"},
    "role_input": {"en": "input", "tr": "girdi"},
    "role_relay": {"en": "relay", "tr": "aktarıcı"},
    "role_output": {"en": "output", "tr": "çıktı"},
    "role_unknown": {"en": "unknown", "tr": "bilinmiyor"},
}


def t(key: str, lang: str = "en", **kwargs) -> str:
    entry = STRINGS.get(key)
    if entry is None:
        return key
    text = entry.get(lang, entry.get("en", key))
    return text.format(**kwargs) if kwargs else text
