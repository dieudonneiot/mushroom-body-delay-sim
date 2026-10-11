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
    "opt_connectome": {
        "en": "Bundled connectome (Princeton export)",
        "tr": "Dahil edilen konektom (Princeton dışa aktarımı)",
    },
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
    "tab_propagation": {"en": "Live Propagation", "tr": "Canlı Yayılım"},
    "caption_propagation": {
        "en": (
            "Press ▶ Play to watch the signal spread through both networks on a shared "
            "simulated-time axis — the damaged network visibly falls behind as it plays. "
            "Nodes light up (colored by role) the instant they fire; drag the slider to "
            "scrub manually."
        ),
        "tr": (
            "Sinyalin her iki ağda da ortak bir simüle-zaman ekseninde nasıl yayıldığını "
            "izlemek için ▶ Oynat'a basın — hasarlı ağın oynatma sırasında geride kaldığı "
            "açıkça görülür. Nöronlar ateşlendiği anda (role göre renklendirilmiş olarak) "
            "yanar; elle gezinmek için kaydırıcıyı sürükleyin."
        ),
    },
    "anim_play": {"en": "▶ Play", "tr": "▶ Oynat"},
    "anim_pause": {"en": "⏸ Pause", "tr": "⏸ Duraklat"},
    "anim_time_prefix": {"en": "Simulated time", "tr": "Simüle edilmiş zaman"},
    "anim_fired_healthy": {"en": "Healthy fired", "tr": "Sağlıklıda ateşlenen"},
    "anim_fired_damaged": {"en": "Damaged fired", "tr": "Hasarlıda ateşlenen"},
    "label_anim_speed": {
        "en": "Playback speed (ms per frame — higher is slower)",
        "tr": "Oynatma hızı (kare başına ms — yüksek değer daha yavaş)",
    },
    "col_node": {"en": "Neuron ID", "tr": "Nöron Kimliği"},
    "col_healthy_time": {"en": "Healthy time", "tr": "Sağlıklı zaman"},
    "col_damaged_time": {"en": "Damaged time", "tr": "Hasarlı zaman"},
    "col_pct_deviation": {"en": "% deviation", "tr": "% sapma"},
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
    "metric_damaged_threshold": {
        "en": "Damaged firing threshold",
        "tr": "Hasarlı ateşleme eşiği",
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
    "expander_absolute_times": {
        "en": "Show absolute arrival times (healthy vs. damaged, side by side)",
        "tr": "Mutlak varış zamanlarını göster (sağlıklı ve hasarlı, yan yana)",
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
    "colorbar_delay_delta": {"en": "Δ delay (damaged − healthy)", "tr": "Δ gecikme (hasarlı − sağlıklı)"},
    "hover_damaged_time": {"en": "damaged time", "tr": "hasarlı zaman"},
    "hover_delay_delta": {"en": "Δ delay", "tr": "Δ gecikme"},
    "chart_delta_title": {"en": "Delay difference (damaged − healthy)", "tr": "Gecikme farkı (hasarlı − sağlıklı)"},
    "caption_delta_chart": {
        "en": (
            "Colored by how much later (red) or earlier (blue) each neuron fired in the "
            "damaged network vs. the healthy one — this is the direct answer to \"where does "
            "the damage show up,\" which two separately-colored healthy/damaged plots make "
            "hard to see at a glance on a large graph."
        ),
        "tr": (
            "Her nöronun hasarlı ağda sağlıklı ağa kıyasla ne kadar daha geç (kırmızı) veya "
            "daha erken (mavi) ateşlendiğine göre renklendirilmiştir — bu, büyük bir grafikte "
            "ayrı renklendirilmiş iki sağlıklı/hasarlı grafiğin tek bakışta göstermesi zor olan "
            "\"hasar nerede ortaya çıkıyor\" sorusuna doğrudan cevap verir."
        ),
    },
    "role_input": {"en": "input", "tr": "girdi"},
    "role_relay": {"en": "relay", "tr": "aktarıcı"},
    "role_output": {"en": "output", "tr": "çıktı"},
    "role_modulatory": {"en": "modulatory", "tr": "düzenleyici"},
    "role_unknown": {"en": "unknown", "tr": "bilinmiyor"},
    # Perturbation panel
    "header_perturbations": {"en": "Perturbations", "tr": "Bozulmalar"},
    "btn_add_perturbation": {"en": "＋ Add Perturbation", "tr": "＋ Bozulma Ekle"},
    "btn_remove_perturbation": {"en": "✕ Remove", "tr": "✕ Kaldır"},
    "label_perturbation_type": {"en": "Impairment", "tr": "Bozulma tipi"},
    "label_intensity": {"en": "Intensity (%)", "tr": "Şiddet (%)"},
    "msg_no_perturbations": {
        "en": "No perturbations added yet — click “＋ Add Perturbation” to model a biological impairment.",
        "tr": "Henüz bozulma eklenmedi — bir biyolojik bozulmayı modellemek için “＋ Bozulma Ekle”ye tıklayın.",
    },
    "caption_velocity_severity": {
        "en": "Conduction-velocity channel (Tau, Amyloid): {n_targeted}/{n_total} edges affected (mean severity {pct}%)",
        "tr": "İletim hızı kanalı (Tau, Amiloid): {n_targeted}/{n_total} bağlantı etkilendi (ortalama şiddet %{pct})",
    },
    "caption_threshold_severity": {
        "en": "Firing-threshold channel (GABA, APL): {n_targeted}/{n_total} neurons affected (mean severity {pct}%)",
        "tr": "Ateşleme eşiği kanalı (GABA, APL): {n_targeted}/{n_total} nöron etkilendi (ortalama şiddet %{pct})",
    },
    "label_apl_root_ids": {
        "en": "APL target root_id(s) (comma-separated)",
        "tr": "APL hedef root_id('leri) (virgülle ayrılmış)",
    },
    "help_apl_root_ids": {
        "en": (
            "APL has no dedicated label in Codex's classification export — look it up by "
            "name on codex.flywire.ai and paste its root_id here. Without one, this "
            "perturbation currently has zero effect (see mbsim/targeting.py)."
        ),
        "tr": (
            "APL, Codex'in sınıflandırma dışa aktarımında ayrı bir etikete sahip değildir — "
            "codex.flywire.ai'de ada göre arayıp root_id'sini buraya yapıştırın. Girilmezse "
            "bu bozulmanın şu anda hiçbir etkisi olmaz (bkz. mbsim/targeting.py)."
        ),
    },
    "perturbation_tau": {"en": "Tau Protein", "tr": "Tau Proteini"},
    "perturbation_tau_desc": {
        "en": (
            "Hyperphosphorylated tau tangles disrupting axonal transport — "
            "modeled as reduced conduction velocity."
        ),
        "tr": (
            "Aksonal taşımayı bozan hiperfosforile tau yumakları — "
            "azalmış iletim hızı olarak modellenir."
        ),
    },
    "perturbation_amyloid": {"en": "Beta-Amyloid", "tr": "Beta-Amiloid"},
    "perturbation_amyloid_desc": {
        "en": (
            "Amyloid-beta plaque buildup impairing synaptic transmission — "
            "modeled as reduced conduction velocity."
        ),
        "tr": (
            "Sinaptik iletimi bozan amiloid-beta plak birikimi — "
            "azalmış iletim hızı olarak modellenir."
        ),
    },
    "perturbation_gaba": {"en": "GABA Dysfunction", "tr": "GABA İşlev Bozukluğu"},
    "perturbation_gaba_desc": {
        "en": (
            "Reduced inhibitory GABAergic signaling in the Mushroom Body circuit — "
            "modeled as an increased firing threshold (a noisier baseline a signal "
            "must clear), not a velocity change."
        ),
        "tr": (
            "Mantar Cisimciği devresinde azalmış inhibitör GABAerjik sinyalleşme — "
            "iletim hızı değişimi değil, artmış ateşleme eşiği (bir sinyalin geçmesi "
            "gereken daha gürültülü bir taban çizgisi) olarak modellenir."
        ),
    },
    "perturbation_apl": {"en": "APL Neuron Impairment", "tr": "APL Nöron Bozulması"},
    "perturbation_apl_desc": {
        "en": (
            "Weakened Anterior Paired Lateral neuron feedback inhibition — "
            "modeled as an increased firing threshold (a noisier baseline a signal "
            "must clear), not a velocity change."
        ),
        "tr": (
            "Zayıflamış Anterior Paired Lateral nöron geri besleme inhibisyonu — "
            "iletim hızı değişimi değil, artmış ateşleme eşiği (bir sinyalin geçmesi "
            "gereken daha gürültülü bir taban çizgisi) olarak modellenir."
        ),
    },
    # Perception & Delay tab
    "tab_perception": {"en": "Perception & Delay", "tr": "Algı ve Gecikme"},
    "header_physical_delay": {"en": "Physical Conduction Delay", "tr": "Fiziksel İletim Gecikmesi"},
    "metric_healthy_delay_ms": {"en": "Healthy delay (ms)", "tr": "Sağlıklı gecikme (ms)"},
    "metric_damaged_delay_ms": {"en": "Damaged delay (ms)", "tr": "Hasarlı gecikme (ms)"},
    "metric_net_delay_ms": {"en": "Net delay (Δms)", "tr": "Net gecikme (Δms)"},
    "header_weber_fechner": {
        "en": "Weber-Fechner Time Perception Deviation",
        "tr": "Weber-Fechner Zaman Algısı Sapması",
    },
    "caption_weber_fechner": {
        "en": (
            "Perceived vs. physical time under the Weber-Fechner law, healthy vs. damaged "
            "(placeholder model — see mbsim/perception.py)."
        ),
        "tr": (
            "Weber-Fechner yasasına göre algılanan ve fiziksel zaman, sağlıklı ve hasarlı "
            "(yer tutucu model — bkz. mbsim/perception.py)."
        ),
    },
    "chart_weber_fechner_title": {
        "en": "Time perception deviation: {pct}%",
        "tr": "Zaman algısı sapması: %{pct}",
    },
    "axis_physical_time": {"en": "Physical time (s, log scale)", "tr": "Fiziksel zaman (s, logaritmik)"},
    "axis_perceived_time": {
        "en": "Perceived time (arbitrary units, placeholder model)",
        "tr": "Algılanan zaman (keyfi birim, yer tutucu model)",
    },
    "metric_deviation_pct": {"en": "Time perception deviation", "tr": "Zaman algısı sapması"},
    "header_calibration": {"en": "Calibration (placeholder)", "tr": "Kalibrasyon (yer tutucu)"},
    "caption_calibration_source": {
        "en": (
            "Default sourced from mbsim/calibration.py (a literature-anchored placeholder, "
            "not a measurement) — override below for what-if exploration. Replace the "
            "module once Phase 2 lab timing data is available."
        ),
        "tr": (
            "Varsayılan değer mbsim/calibration.py'den alınır (literatüre dayanan bir yer "
            "tutucu, bir ölçüm değil) — ne-olur-ne-olmaz keşfi için aşağıdan geçersiz kılın. "
            "Faz 2 laboratuvar zamanlama verisi elde edildiğinde bu modülü değiştirin."
        ),
    },
    "label_ms_calibration": {
        "en": "Milliseconds per simulated time unit",
        "tr": "Simüle edilmiş zaman birimi başına milisaniye",
    },
    "header_trials": {
        "en": "Trial-based Weber fraction estimate (Monte Carlo)",
        "tr": "Deneme-tabanlı Weber kesri tahmini (Monte Carlo)",
    },
    "caption_trials": {
        "en": (
            "The point-estimate deviation above compares one healthy run to one damaged run. "
            "A Weber fraction is properly a variability measure across *repeated* trials — "
            "this runs N independent noisy trials per side and reports the coefficient of "
            "variation (std/mean arrival time) as an empirical Weber-fraction-like estimate. "
            "The noise model is a placeholder (see mbsim/trials.py), not literature-calibrated."
        ),
        "tr": (
            "Yukarıdaki nokta-tahmini sapma, bir sağlıklı çalıştırmayı bir hasarlı "
            "çalıştırmayla karşılaştırır. Weber kesri asıl olarak *tekrarlanan* denemeler "
            "arasındaki bir değişkenlik ölçüsüdür — bu, her taraf için N bağımsız gürültülü "
            "deneme çalıştırır ve değişim katsayısını (std/ortalama varış zamanı) ampirik bir "
            "Weber-kesri-benzeri tahmin olarak bildirir. Gürültü modeli bir yer tutucudur "
            "(bkz. mbsim/trials.py), literatüre göre kalibre edilmemiştir."
        ),
    },
    "label_n_trials": {"en": "Number of trials", "tr": "Deneme sayısı"},
    "label_noise_std": {"en": "Noise (log-std)", "tr": "Gürültü (log-std)"},
    "btn_run_trials": {"en": "▶ Run trials", "tr": "▶ Denemeleri çalıştır"},
    "spinner_running_trials": {
        "en": "Running noisy trials — this can take a while on large graphs...",
        "tr": "Gürültülü denemeler çalıştırılıyor — büyük graflarda biraz zaman alabilir...",
    },
    "metric_healthy_weber_fraction": {
        "en": "Healthy Weber fraction (empirical)",
        "tr": "Sağlıklı Weber kesri (ampirik)",
    },
    "metric_damaged_weber_fraction": {
        "en": "Damaged Weber fraction (empirical)",
        "tr": "Hasarlı Weber kesri (ampirik)",
    },
    "caption_trials_not_run": {
        "en": "Not run yet — click “▶ Run trials” above.",
        "tr": "Henüz çalıştırılmadı — yukarıdan “▶ Denemeleri çalıştır”a tıklayın.",
    },
    "info_zero_severity": {
        "en": "No active perturbations — healthy and damaged curves are identical, so 0% deviation is expected here, not a bug.",
        "tr": "Etkin bozulma yok — sağlıklı ve hasarlı eğriler aynı, bu yüzden burada %0 sapma beklenen bir durumdur, hata değildir.",
    },
    "warn_high_severity": {
        "en": (
            "Combined severity is at or near 100% — this models near-total conduction "
            "blockage, so delay/deviation numbers below will look extreme by design, not "
            "because of an error."
        ),
        "tr": (
            "Birleşik şiddet %100'e yakın veya eşit — bu, iletimin neredeyse tamamen "
            "durduğunu modeller, bu yüzden aşağıdaki gecikme/sapma sayıları bir hata değil, "
            "tasarım gereği aşırı görünecektir."
        ),
    },
    # Validation (Phase 2/3) tab
    "tab_validation": {"en": "Phase 2/3 Validation", "tr": "Faz 2/3 Doğrulama"},
    "caption_validation": {
        "en": (
            "Compare this simulation's % deviation against Phase 2 fly lab data and/or "
            "Phase 3 human clinical data, once collected. The goal is a same-direction, "
            "meaningful-magnitude match, not an exact percentage (see mbsim/validation.py)."
        ),
        "tr": (
            "Bu simülasyonun % sapmasını, toplandığında Faz 2 sinek laboratuvar verisi "
            "ve/veya Faz 3 insan klinik verisiyle karşılaştırın. Hedef, tam bir yüzde "
            "eşleşmesi değil, aynı yönde ve anlamlı büyüklükte bir eşleşmedir "
            "(bkz. mbsim/validation.py)."
        ),
    },
    "label_climbing_upload": {
        "en": "Phase 2 climbing assay CSV (optional)",
        "tr": "Faz 2 tırmanma deneyi CSV'si (isteğe bağlı)",
    },
    "help_climbing_upload": {
        "en": "Columns: group (control/alzheimers_model), fly_id, trial, climb_time_s — see data/lab/README.md.",
        "tr": "Sütunlar: group (control/alzheimers_model), fly_id, trial, climb_time_s — bkz. data/lab/README.md.",
    },
    "label_clinical_upload": {
        "en": "Phase 3 time-perception task CSV (optional)",
        "tr": "Faz 3 zaman algısı görevi CSV'si (isteğe bağlı)",
    },
    "help_clinical_upload": {
        "en": (
            "Columns: patient_id, group (control/alzheimers), target_interval_s, "
            "reported_time_s, simple_reaction_time_s — see data/clinical/README.md."
        ),
        "tr": (
            "Sütunlar: patient_id, group (control/alzheimers), target_interval_s, "
            "reported_time_s, simple_reaction_time_s — bkz. data/clinical/README.md."
        ),
    },
    "btn_load_example_validation": {
        "en": "▶ Load synthetic example data (not real lab/clinical results)",
        "tr": "▶ Sentetik örnek veriyi yükle (gerçek laboratuvar/klinik sonucu değildir)",
    },
    "caption_example_validation": {
        "en": "Showing the synthetic example dataset — upload real CSVs above to replace it.",
        "tr": "Sentetik örnek veri seti gösteriliyor — gerçek CSV'leri yukarıdan yükleyerek değiştirin.",
    },
    "info_no_validation_data": {
        "en": (
            "No Phase 2/3 data yet — upload a CSV above, or click “▶ Load synthetic example "
            "data” to see how this comparison will look once real data exists."
        ),
        "tr": (
            "Henüz Faz 2/3 verisi yok — yukarıdan bir CSV yükleyin veya gerçek veri elde "
            "edildiğinde bu karşılaştırmanın nasıl görüneceğini görmek için “▶ Sentetik örnek "
            "veriyi yükle”ye tıklayın."
        ),
    },
    "err_validation_load": {
        "en": "Could not read the uploaded file: {error}",
        "tr": "Yüklenen dosya okunamadı: {error}",
    },
    "warn_validation_no_sim_deviation": {
        "en": "The simulation reached no output neurons, so there is no simulated % deviation to compare against.",
        "tr": "Simülasyon hiçbir çıktı nöronuna ulaşmadı, bu yüzden karşılaştırılacak bir simüle % sapma yok.",
    },
    "metric_sim_deviation": {"en": "Simulation % deviation", "tr": "Simülasyon % sapması"},
    "metric_fly_deviation": {"en": "Phase 2 fly % deviation", "tr": "Faz 2 sinek % sapması"},
    "metric_human_deviation": {
        "en": "Phase 3 human excess % deviation",
        "tr": "Faz 3 insan fazladan % sapması",
    },
    "label_same_direction": {"en": "Same direction as simulation?", "tr": "Simülasyonla aynı yönde mi?"},
    "same_direction_yes": {"en": "✅ Yes", "tr": "✅ Evet"},
    "same_direction_no": {"en": "❌ No", "tr": "❌ Hayır"},
}


def t(key: str, lang: str = "en", **kwargs) -> str:
    entry = STRINGS.get(key)
    if entry is None:
        return key
    text = entry.get(lang, entry.get("en", key))
    return text.format(**kwargs) if kwargs else text
