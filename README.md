# Mushroom Body Signal-Delay Simulation

**▶ Live app / Canlı uygulama: [mb-delay-sim.streamlit.app](https://mb-delay-sim.streamlit.app/?embed=true)** — runs in the browser, nothing to install / tarayıcıda çalışır, kurulum gerekmez.

**🇬🇧 [English](#english) &nbsp;|&nbsp; 🇹🇷 [Türkçe](#türkçe) &nbsp;|&nbsp; 📖 [Glossary / Sözlük](#glossary-of-key-terms--anahtar-terimler-sözlüğü)**

---

## Glossary of Key Terms / Anahtar Terimler Sözlüğü

| Term | English | Türkçe |
|---|---|---|
| **Connectome** | A complete map of neural connections (nodes = neurons, edges = synapses) in a brain or part of a brain. | Bir beynin veya beyin bölümünün tam nöral bağlantı haritası (düğümler = nöronlar, kenarlar = sinapslar). |
| **FlyWire / Codex** | The public database (codex.flywire.ai) hosting the full synaptic-resolution connectome of the fruit fly (*Drosophila*) brain. | *Drosophila* (meyve sineği) beyninin sinaptik çözünürlükteki tam konektomunu barındıran halka açık veritabanı (codex.flywire.ai). |
| **Mushroom Body (MB)** | A paired brain structure in insects responsible for memory, learning, and multisensory integration — the focus of this simulation. | Böceklerde bellek, öğrenme ve çoklu-duyusal entegrasyondan sorumlu, çift yapılı beyin bölgesi — bu simülasyonun odak noktası. |
| **PN** (Projection Neuron) | A neuron carrying sensory (e.g. olfactory) information into the Mushroom Body; the default **input** role. | Duyusal (örn. koku) bilgisini Mantar Cisimciği'ne taşıyan nöron; varsayılan **girdi** rolü. |
| **KC** (Kenyon Cell) | The principal intrinsic neuron of the Mushroom Body; acts as the relay/associative layer between PNs and MBONs — the default **relay** role. | Mantar Cisimciği'nin başlıca içsel nöronu; PN'ler ile MBON'lar arasında aktarıcı/ilişkilendirici katman görevi görür — varsayılan **aktarıcı** rolü. |
| **MBON** (Mushroom Body Output Neuron) | A neuron carrying the Mushroom Body's output signal onward to the rest of the brain — the default **output** role, where signal delay is measured. | Mantar Cisimciği'nin çıktı sinyalini beynin geri kalanına ileten nöron — varsayılan **çıktı** rolü, sinyal gecikmesinin ölçüldüğü yer. |
| **MBIN / DAN** (dopaminergic neuron) | A modulatory (often dopaminergic) neuron signaling reward/punishment to shape Kenyon cell activity; available as a cell type but not used by default. | Kenyon hücresi etkinliğini şekillendirmek için ödül/ceza sinyali veren düzenleyici (genellikle dopaminerjik) nöron; bir hücre tipi olarak mevcuttur ama varsayılan olarak kullanılmaz. |
| **Neuropil** | A region of densely packed neural tissue (synapses, dendrites, axons) with little cell-body content. | Yoğun nöral doku (sinaps, dendrit, akson) içeren, hücre gövdesi az olan bölge. |
| **Synapse count** (`syn_count`) | The number of synaptic contacts between two neurons; used here as the edge "weight" — more synapses roughly means a stronger, faster connection. | İki nöron arasındaki sinaptik temas sayısı; burada kenar "ağırlığı" olarak kullanılır — daha fazla sinaps, kabaca daha güçlü ve daha hızlı bir bağlantı demektir. |
| **Root ID** (`root_id`) | The unique identifier FlyWire assigns to each segmented neuron in the connectome. | FlyWire'ın konektomdaki her bölütlenmiş nörona atadığı benzersiz kimlik numarası. |
| **Cell type** | The functional/anatomical classification of a neuron (e.g. PN, KC, MBON); used to assign each neuron's role in this simulation. | Bir nöronun işlevsel/anatomik sınıflandırması (örn. PN, KC, MBON); bu simülasyonda her nöronun rolünü atamak için kullanılır. |
| **Node / Edge** | Graph-theory terms: a node is a neuron, an edge is a synaptic connection between two neurons. | Graf teorisi terimleri: düğüm bir nörondur, kenar iki nöron arasındaki sinaptik bağlantıdır. |
| **Role** (input / relay / output) | This project's label for where a neuron sits in the simulated pathway: *input* = where the signal starts, *relay* = the middle layer, *output* = where arrival time is measured. | Bu projede bir nöronun simüle edilen yolaktaki konumunu belirten etiket: *girdi* = sinyalin başladığı yer, *aktarıcı* = ara katman, *çıktı* = varış zamanının ölçüldüğü yer. |
| **Conduction velocity** | How fast a signal travels along a connection; the simulation's speed parameter, reduced by the Tau/Amyloid perturbations. | Bir sinyalin bağlantı boyunca ne kadar hızlı ilerlediği; Tau/Amiloid bozulmalarıyla azaltılan simülasyon hız parametresi. |
| **Firing threshold** | The amount of accumulated incoming signal a neuron needs before it "fires" and forwards the signal onward. | Bir nöronun "ateşlenip" sinyali sonraki nöronlara iletmesi için ihtiyaç duyduğu birikmiş gelen sinyal miktarı. |
| **Perturbation / intensity** | One Alzheimer's-like impairment (Tau, Beta-Amyloid, GABA, APL) added in the app's Perturbations panel, with an intensity from 0% (none) to 100% (maximum). Several can be stacked. Mapped through placeholder linear functions for now. | Uygulamanın Bozulmalar panelinden eklenen, Alzheimer benzeri tek bir bozulma (Tau, Beta-Amiloid, GABA, APL) ve %0 (yok) ile %100 (maksimum) arasındaki şiddeti. Birden fazlası üst üste eklenebilir. Şimdilik yer tutucu doğrusal fonksiyonlar üzerinden hesaplanır. |
| **Slowdown function** | The pluggable function (in `damage.py`) converting a severity value into a conduction-velocity reduction; meant to be replaced with a literature-derived one. | Bir şiddet değerini iletim hızı azalmasına dönüştüren, eklenebilir (`damage.py` içindeki) fonksiyon; literatüre dayalı bir fonksiyonla değiştirilmek üzere tasarlanmıştır. |
| **Arrival time** | The simulated time at which a signal first reaches (and "fires") a given neuron, measured from t=0 at the input neurons. | Bir sinyalin, girdi nöronlarında t=0'dan başlayarak belirli bir nörona ilk ulaştığı (ve "ateşlendiği") simüle edilmiş zaman. |
| **% deviation** | How much later the damaged network's arrival time is compared to the healthy network's, as a percentage. | Hasarlı ağın varış zamanının, sağlıklı ağa kıyasla yüzde kaç daha geç olduğu. |
| **Healthy / damaged network** | The same Mushroom Body graph simulated twice: once at the baseline conduction velocity ("healthy"), once with severity-reduced conduction velocity ("damaged"). | Aynı Mantar Cisimciği grafiğinin iki kez simüle edilmesi: biri temel iletim hızıyla ("sağlıklı"), diğeri şiddetle azaltılmış iletim hızıyla ("hasarlı"). |
| **Fixture** (demo data) | The small synthetic connectome bundled with the project so it can run without the real Codex download. | Gerçek Codex indirmesi olmadan projeyi çalıştırabilmek için pakete dahil edilen küçük sentetik konektom verisi. |
| **CLI** (batch mode) | Running the pipeline from the terminal (`python -m mbsim.cli`) with a config file, producing static output files, as opposed to the live interactive app. | İşlem hattını, canlı etkileşimli uygulamanın aksine, bir yapılandırma dosyasıyla terminalden (`python -m mbsim.cli`) çalıştırıp statik çıktı dosyaları üretmek. |
| **Sanity report** | A quick printed summary of the extracted graph (node/edge counts, role breakdown, isolated nodes) used to catch bad data/role filtering early. | Kötü veri/rol filtrelemesini erken yakalamak için kullanılan, çıkarılan grafiğin (düğüm/kenar sayıları, rol dağılımı, izole düğümler) hızlı bir yazdırılmış özeti. |
| **ALPN / Kenyon_Cell / DAN / MBIN** (real-data labels) | The `class` values real Codex exports use for the roles this project calls PN, KC, and the optional modulatory pathway; the fixture uses the simpler PN/KC/MBON names instead. | Gerçek Codex dışa aktarımlarının, bu projede PN, KC ve isteğe bağlı düzenleyici yolak için kullandığı `class` değerleri; örnek veri (fixture) bunun yerine daha basit PN/KC/MBON adlarını kullanır. |
| **Live Propagation** (animation) | The animated, side-by-side playback of signal arrival over simulated time, comparing healthy vs. damaged networks frame by frame. | Sağlıklı ve hasarlı ağları kare kare karşılaştıran, simüle edilmiş zaman üzerinden sinyal varışının canlandırılmış, yan yana oynatımı. |

---

## English

Simulates how Alzheimer's-driven slowing of neuronal conduction velocity delays
signal transit through the Drosophila Mushroom Body (the fly's memory/learning
center), using the FlyWire/Codex connectome (https://codex.flywire.ai).

Pipeline: connectome CSVs -> Mushroom Body pathway subgraph (e.g. PN -> KC -> MBON)
-> event-driven signal propagation -> healthy vs. damaged comparison, in both an
interactive UI and a batch CLI.

### What the system does

1. **Loads a real fly-brain wiring map.** The app ships with a subset of the
   FlyWire/Codex connectome: 5,958 Mushroom Body neurons (685 ALPN input,
   5,177 Kenyon cell relay, 96 MBON output) and 79,423 synaptic connections.
2. **Sends a signal through it twice.** It runs the signal once through a
   healthy network and once through a damaged copy, then records when each
   output neuron fires.
3. **Applies Alzheimer's-like damage.** You choose the damage in the
   **Perturbations** panel. *Tau* and *Beta-Amyloid* slow conduction, while
   *GABA* and *APL* raise the firing threshold. Each one has its own
   intensity from 0 to 100%, and you can stack several.
4. **Measures the result.** It reports the extra delay in milliseconds, the %
   deviation per output neuron, a Weber-Fechner time-perception estimate, and
   an animated side-by-side playback of the two networks.

All damage curves, the ms calibration and the perception model are
**placeholders** until literature or lab values are available. The numbers
show how the model behaves; they are not clinical predictions.

### Quick start

- **Just use it:** open [mb-delay-sim.streamlit.app](https://mb-delay-sim.streamlit.app/?embed=true). The real
  connectome loads by default, and you can switch the language to Türkçe at
  the top of the sidebar.
- **Test it:** follow the checklist in [section 8](#8-how-to-test).
- **Run or develop it locally:** see Setup below.

### 1. Setup (local development only)

```
git clone https://github.com/dieudonneiot/mushroom-body-delay-sim.git
cd mushroom-body-delay-sim
python -m venv .venv
.venv/Scripts/activate   # .venv/bin/activate on macOS/Linux
pip install -e ".[dev]"
```

Requires Python 3.10+. The repository is public, so anyone can clone it. You
only need a local setup to change the code or run the tests; to use the app,
open the live link above.

This installs the `mbsim` package plus `streamlit`, `plotly`, `networkx`, `pandas`,
`matplotlib`, `pyyaml`, and (via `[dev]`) `pytest`.

If you ever move or rename the project folder after the `.venv` already
exists, delete and recreate it (`rm -rf .venv` then repeat the two commands
above) — the venv's `pip`/`streamlit`/etc. launchers hardcode an absolute
path at creation time and silently break ("Fatal error in launcher") if that
path stops existing.

### 2. Getting the real connectome data

Codex does not offer a general bulk API — data is exported manually as CSV.
Log in at https://codex.flywire.ai, open **Downloadable assets** (the download
icon in the top bar), pick the `FAFB` dataset, and grab exactly two files:

- **"Connections (Filtered)"** → save as `data/raw/connections.csv`
- **"Classification / Hierarchical Annotations"** → save as `data/raw/classification.csv`

Skip everything else on that page — "Synapse Table" and "Neuron Skeletons" are
multi-gigabyte and this pipeline never reads either. Full details (including a
schema gotcha) are in [data/raw/README.md](data/raw/README.md); short version:
the real Codex export has **no `cell_type` column** — it has `class` instead,
with values `ALPN` (input, ≈ the fixture's `PN`), `Kenyon_Cell` (relay, ≈ `KC`),
`MBON` (output), plus `DAN`/`MBIN` if you want the modulatory dopaminergic
pathway too. `mbsim.io` aliases `class` → `cell_type` automatically, so no
manual CSV editing is needed — you only need the real label names when
picking pathway roles (in the UI or a config file).

Once both files are in place, either edit `configs/default.yaml`
(`data.mode: raw`, and update `roles` to the real labels) or just use the
ready-made [configs/raw.yaml](configs/raw.yaml), which already has both set —
see "CLI" below.

You don't need this step to use the app. A ready-made real-data subset is
already in `data/connectome/` and loads by default (see
[data/connectome/README.md](data/connectome/README.md)), and the small
synthetic graph in `data/fixtures/` (3 PN, 6 KC, 2 MBON neurons, fully wired)
is always available for quick checks.

### 3. Interactive UI

The app is deployed on Streamlit Community Cloud at
[mb-delay-sim.streamlit.app](https://mb-delay-sim.streamlit.app/?embed=true) and redeploys automatically on every push
to `main`. To run it locally instead:

```
streamlit run app.py
```

Every detail of what's on screen:

**Language toggle** — at the very top of the sidebar, a switch between
**English** and **Türkçe**. It re-translates every label, button, tab, warning,
chart title, and even the graph hover tooltips — nothing is left in the other
language. Switch it anytime; your other settings (sliders, data source) are kept.

**Sidebar — Data source**
- *Bundled connectome (Princeton export)* — the compact, real-data ALPN/Kenyon_Cell/MBON subset in `data/connectome/`; this is the default and ships with the Community Cloud app.
- *Fixture (demo data)* — the small synthetic graph in `data/fixtures/`, always available for a quick demo.
- *data/raw/ (local files)* — shown only when both CSVs exist in `data/raw/`; useful for local development with a full export.
- *Upload CSVs* — two file-upload widgets appear; drop in your own `connections.csv` and `classification.csv` directly from your computer (no need to place them in the repo folder at all). Useful for trying a different Codex dataset release or a subset someone emailed you.

**Sidebar — Mushroom Body pathway**
Once data is loaded, three dropdown (multi-select) pickers appear, pre-populated
with every distinct `cell_type` value found in your data:
- *Input cell type(s)* — which neuron types the signal starts at (defaults to `PN` if present).
- *Relay cell type(s)* — the middle layer the signal passes through (defaults to `KC`).
- *Output cell type(s)* — where signal arrival time is measured (defaults to `MBON`).

You can select more than one type per role (e.g. multiple input types), and
change these freely if your dataset uses different labels — nothing is
hardcoded to PN/KC/MBON, those are just the defaults when present.

**Sidebar — Simulation parameters** (all update the view live, no button to press)
- *Healthy conduction velocity* (0.1–3.0, default 1.0) — baseline signal speed in the undamaged network. Higher = faster signal.
- *Firing threshold* (0.5–5.0, default 1.0) — how much accumulated incoming signal a neuron needs before it "fires" and forwards the signal onward.
**Sidebar — Perturbations** (the Alzheimer's-damage controls)
- Click **＋ Add Perturbation** to add a damage row. Pick its *Impairment* type and set an *Intensity (%)* from 0 to 100 with the slider or the number box. Rows stack, and the **✕** button removes one.
  - *Tau Protein* and *Beta-Amyloid* lower conduction velocity on the edges they target.
  - *GABA Dysfunction* and *APL Neuron Impairment* raise the firing threshold on the neurons they target. APL needs a root_id typed into its field, otherwise it has no effect.
- With no rows, healthy and damaged are identical, so a 0% deviation is expected.
- The captions above the tabs show how many edges and neurons each channel affects and the mean severity.
- Intensities map through placeholder linear curves in `mbsim/damage.py`; see "Extending with a real damage model" below.
- *Calibration (placeholder)* expander: milliseconds per simulated time unit, used for the ms readouts.

**Main area — "Perception & Delay" tab** (opens first)
- *Physical Conduction Delay*: mean healthy delay, mean damaged delay and the net Δ, all in ms.
- *Weber-Fechner Time Perception Deviation*: perceived-vs-physical time curves for healthy and damaged, with the % deviation. This uses a placeholder model (`mbsim/perception.py`).
- *Trial-based Weber fraction estimate* expander: runs N noisy trials when you click **▶ Run trials** (see section 6).

**Main area — "Network View" tab**
- Five KPI cards at the top: mean and median % delay deviation, the mean damaged conduction velocity and the mean damaged firing threshold over the targeted edges and neurons (shown as `n/a` when that channel isn't used), and how many output neurons the signal reached out of the total.
- A **delay-difference** network graph laid out left to right (input → relay → output). Each neuron is colored by how much later (red) or earlier (blue) it fired in the damaged network than in the healthy one. **Hover over any neuron** to see its id, role, in- and out-degree and arrival times. **Scroll or drag to zoom and pan.**
- A collapsible "Show absolute arrival times" panel holds the healthy and damaged graphs side by side, colored by arrival time on a shared scale. Gray nodes were never reached.
- A collapsible "Show pathway structure" panel shows the same graph colored by role, so you can inspect the wiring without any simulation overlay.
- Marker size, node labels, and edge opacity all scale down automatically on large graphs (real-connectome scale: thousands of nodes, tens of thousands of edges), so the view stays legible instead of rendering as a solid blob — no configuration needed.

**Main area — "Comparison" tab**
A grouped bar chart: healthy vs. damaged arrival time, one pair of bars per
output neuron. This is the chart form of the same numbers as the CSV in the
"Data" tab.

**Main area — "Data" tab**
The raw comparison table (one row per output neuron reached: healthy time,
damaged time, % deviation), translated column headers matching your chosen
language, plus a "Download comparison.csv" button to save it locally (with
stable English column names, for reprocessing elsewhere) for further analysis
or sharing with the medical team.

**Main area — "Live Propagation" tab**
An animated, side-by-side playback of the signal spreading through the
healthy and damaged networks on a shared simulated-time axis. Press **▶ Play**
(top-left of the chart) to watch neurons light up — colored by role, the
instant they fire — or drag the slider under the chart to scrub to any
instant manually. A running readout above the charts
(`t = ... | Healthy fired: X/Y | Damaged fired: X/Y`) makes the damaged
network's lag legible as an exact number, not just a subtle visual
difference, and a vertical divider line makes it unambiguous that two
separate networks are shown side by side. Frames are spaced by *quantile of
fire time*, not linearly in time: real fire-time distributions are heavily
front-loaded (most of the network fires almost immediately, then a long tail
of stragglers), so quantile spacing means each frame reveals a similar number
of newly-active nodes — a smooth, evenly-paced wave instead of one flash
followed by dozens of nearly-static frames. A **"Playback speed"** slider
(50–1500ms per frame, default 400ms — higher is slower) lets you slow it down
for a closer look at exactly what's happening.

**Error handling** — if your role selection doesn't match any neurons, or a CSV
is missing an expected column, or no signal reaches any output neuron, you get
a plain-language on-screen message (in whichever language you've selected)
instead of a crash.

### 4. CLI (batch mode)

```
python -m mbsim.cli --config configs/default.yaml
```

Prints a sanity report on the extracted subgraph, then a healthy vs. damaged
signal-delay comparison at the output neurons, and writes
`outputs/comparison.csv`, `outputs/comparison.png`, `outputs/network_structure.png`,
`outputs/network_healthy.png`, `outputs/network_damaged.png` (static matplotlib
images — useful for a report/email, whereas the Streamlit app is for live
exploration).

Once the real connectome is in `data/raw/` (see step 2 above), use the
ready-made [configs/raw.yaml](configs/raw.yaml) instead — same as
`default.yaml` but with `data.mode: raw` and `roles` already set to the real
`ALPN`/`Kenyon_Cell`/`MBON` labels:

```
python -m mbsim.cli --config configs/raw.yaml
```

At real-connectome scale the matplotlib renderer automatically thins edges,
shrinks markers, and drops per-edge arrowheads and per-node labels for both
speed and legibility (see `mbsim/layout.py`) — on the full FAFB Mushroom Body
subgraph (~6,000 nodes, ~79,000 edges) the whole CLI run finishes in well
under a minute.

Edit `configs/default.yaml` (or your own copy, like `configs/raw.yaml`) to
change, without touching code:
- `data.mode`: `fixture` or `raw`
- `roles`: which cell types count as input/relay/output — `PN`/`KC`/`MBON` for
  the fixture, `ALPN`/`Kenyon_Cell`/`MBON` for real Codex data
- `simulation.conduction_velocity`, `simulation.threshold`
- `damage.perturbations`: the same Tau/Amyloid/GABA/APL stack as the app's "+ Add Perturbation" panel (see `configs/default.yaml` for the shape)
- `output.dir`: where results are written

### 5. Extending with a real damage model

Each perturbation (Tau, Amyloid, GABA, APL) is resolved to the *specific*
edges/neurons it plausibly affects before any damage is applied — see
`src/mbsim/targeting.py`'s module docstring for exactly which connectome
field each one uses (Tau/Amyloid default to every edge; GABA targets edges
whose real Codex `nt_type` is `"GABA"`; APL has no default at all, since it
has no dedicated label in the classification export — target it via a
`target_root_ids` root_id looked up by name on codex.flywire.ai). Two
independent channels come out of that: conduction-velocity severity per
edge and firing-threshold severity per node (see `src/mbsim/perturbations.py`).

`src/mbsim/damage.py` has the two placeholder curves that turn those
severities into actual numbers: `linear_slowdown` (velocity reduction) and
`linear_threshold_increase` (threshold increase), both linear in [0, 1].
Once the medical team provides literature-derived functions (severity ->
reduction), write them there and pass as `slowdown_fn`/`threshold_fn` to
`mbsim.metrics.compare(...)` (already wired into both `app.py` and `cli.py`)
— no changes needed anywhere else in the pipeline.

`src/mbsim/calibration.py` holds the one placeholder constant converting the
simulation's abstract time units to milliseconds — replace its body once
real timing data (Phase 2 lab measurements, or a literature figure) exists.

### 6. Trial-based Weber fraction estimate

A single healthy-vs-damaged comparison is a point estimate, not the
variability-across-trials that a Weber fraction actually measures.
`src/mbsim/trials.py`'s `compare_trials` runs N independent noisy trials per
side (placeholder log-normal jitter on conduction velocity — see its module
docstring) and reports the coefficient of variation (std/mean arrival time)
as an empirical Weber-fraction-like number for each condition. In the app,
open the "Trial-based Weber fraction estimate" expander in the Perception
tab and click "▶ Run trials" (gated behind a button since it's ~10-15s on
the full real connectome, not instant like the rest of the UI).

### 7. Validating against Phase 2/3 data, once it exists

`src/mbsim/validation.py` compares the simulation's %-deviation against the
Phase 2 fly climbing-assay %-deviation and/or the Phase 3 human time-
perception-task deviation, reporting whether each empirical source moved in
the *same direction* as the simulation — the project's actual validation
goal (see the module's docstring), not an exact percentage match. Neither
data source exists yet; `data/lab/README.md` and `data/clinical/README.md`
document the expected CSV shape (with empty `.template.csv` files) so
whoever exports that data later knows the format, and `validation.py`'s own
tests exercise the comparison logic now against synthetic data shaped the
same way.

This comparison is also exposed in the app itself — the **"Phase 2/3
Validation"** tab lets you upload a climbing-assay CSV and/or a
time-perception-task CSV (once either exists) and see the simulation's %
deviation compared side by side, with a same-direction check for each. Since
neither data source exists yet, a **"▶ Load synthetic example data"** button
loads a clearly-labeled placeholder dataset instead, so the comparison
mechanism itself can be demonstrated (e.g. for a presentation) before real
data lands.

### 8. How to test

#### A. In the browser (no install, ~5 minutes)

Open [mb-delay-sim.streamlit.app](https://mb-delay-sim.streamlit.app/?embed=true). If it shows a "wake up" button,
the free app was asleep: click it and wait about 30 seconds. Then check each
step against the expected result. The values come from the live app with the
default data source, *Bundled connectome (Princeton export)*.

| # | Do this | Expected result |
|---|---|---|
| 1 | Look at the caption under the title | `Graph: 5958 neurons, 79423 synaptic connections (relay: 5177, output: 96, input: 685)` |
| 2 | Switch the sidebar language to **Türkçe**, then back | Every label, tab and chart title changes language, and your settings stay |
| 3 | Without adding perturbations, open **Perception & Delay** | Healthy and damaged delay are both **0.34 ms**, the deviation is **0%**, and a blue note explains that 0% is expected |
| 4 | Click **＋ Add Perturbation**, keep *Tau Protein*, type **40** in the intensity box | Caption: `79423/79423 edges affected (mean severity 40.0%)`. Delay goes **0.34 → 0.57 ms (+0.23)** and time-perception deviation is **66.7%** |
| 5 | Open the *Trial-based Weber fraction* expander and click **▶ Run trials** | After a few seconds, healthy and damaged Weber fractions appear (about 6% each with the defaults) |
| 6 | **Network View** tab | KPIs: mean and median deviation **66.7%**, damaged velocity **0.600**, threshold `n/a`, outputs reached **96/96**. The graph shows red (later) Kenyon cells |
| 7 | **Comparison** tab | Grouped healthy and damaged bars for each output neuron, with the damaged bar higher everywhere |
| 8 | **Data** tab, then **Download comparison.csv** | 96 rows, each with `% deviation` ≈ 66.67, and a CSV downloads |
| 9 | **Live Propagation** tab: press **▶ Play**, or drag the slider to the middle | At t ≈ 0.056 the readout shows about **4380/5958** neurons fired in the healthy network and **1889/5958** in the damaged one |
| 10 | **Phase 2/3 Validation** tab: click **▶ Load synthetic example data** | Simulation 66.7%, fly 30.0% and human 30.0%, both marked **✅ Yes** (same direction) |
| 11 | Add a second perturbation, **GABA Dysfunction** at 50% (keep Tau at 40%) | Caption: `295/5958 neurons affected (mean severity 50.0%)`. *Damaged firing threshold* becomes **1.500**, and the mean and median deviation rise to **175.2%** and **170.2%** |
| 12 | Set the Tau intensity to **100** | A warning explains that near-total blockage makes the numbers look extreme by design. At 100% Tau, conduction stops, so a "signal never reached an output neuron" message is also expected |
| 13 | Data source → **Fixture (demo data)** | `Graph: 11 neurons, 13 synaptic connections (input: 3, relay: 6, output: 2)`, with roles defaulting to PN/KC/MBON |

#### B. Automated tests (local)

```
pip install -e ".[dev]"
pytest
```

All tests run against the synthetic fixture in `data/fixtures/`, so they don't
need any real Codex download.

#### C. Batch CLI (local)

```
python -m mbsim.cli --config configs/default.yaml
```

This runs on the fixture with a 30% Tau perturbation, prints the comparison and
writes five files under `outputs/`. To run it on the bundled real subset, copy
`configs/raw.yaml` and set `raw_dir: data/connectome`.

If any of these disagree with what's described here, check
`data/connectome/README.md` or `data/raw/README.md` for the expected columns
and file names first.

### Project structure

```
app.py                    # Streamlit interactive UI
src/mbsim/
  io.py                   # load + validate Codex CSV exports
  mushroom_body.py        # filter to the configured input/relay/output pathway
  graph.py                # NetworkX graph construction + sanity checks
  simulation.py           # event-driven signal propagation
  targeting.py            # resolve each perturbation to the specific edges/neurons it affects
  perturbations.py        # named impairments (Tau/Amyloid/GABA/APL) -> per-edge/per-node severity
  damage.py               # severity -> conduction velocity slowdown / firing threshold increase (pluggable)
  calibration.py          # simulated time units -> milliseconds (pluggable)
  metrics.py              # healthy vs. damaged comparison + % deviation
  trials.py               # Monte Carlo trial-to-trial variability -> empirical Weber fraction
  validation.py           # compare simulation output against Phase 2/3 empirical data
  layout.py               # shared node layout / role colors / large-graph scaling
  visualize.py            # static matplotlib figures (used by the CLI)
  plotly_viz.py           # interactive Plotly figures + propagation animation (used by the app)
  i18n.py                 # English/Turkish UI string translations
  inference.py            # Phase A inverse inference (ABC + simulation-based calibration), not in the UI yet
  cli.py                  # batch entrypoint
scripts/prepare_connectome.py  # builds data/connectome/ from raw Codex exports
configs/default.yaml      # CLI configuration (fixture data, PN/KC/MBON roles)
configs/raw.yaml          # CLI configuration for real data (ALPN/Kenyon_Cell/MBON roles)
data/fixtures/            # synthetic demo data (tracked in git)
data/connectome/          # bundled Princeton connectome subset (tracked in git)
data/raw/                 # source Codex exports / local full data (gitignored)
data/lab/                 # Phase 2 fly assay results go here, once collected (gitignored)
data/clinical/            # Phase 3 human task results go here, once collected (gitignored)
tests/                    # pytest suite
```

---

## Türkçe

Alzheimer hastalığının neden olduğu nöral iletim hızı yavaşlamasının, meyve
sineğinin (Drosophila) Mantar Cisimciği (belleğin/öğrenmenin merkezi) üzerinden
sinyal iletimini nasıl geciktirdiğini, FlyWire/Codex konektomunu
(https://codex.flywire.ai) kullanarak simüle eder.

İşlem hattı: konektom CSV dosyaları -> Mantar Cisimciği yolağı alt-grafiği
(örn. PN -> KC -> MBON) -> olay-tabanlı (event-driven) sinyal yayılımı ->
sağlıklı ve hasarlı ağların karşılaştırılması; hem etkileşimli bir arayüzde hem
de toplu (batch) bir CLI aracılığıyla.

### Sistem ne yapar?

1. **Gerçek bir sinek beyni bağlantı haritasını yükler.** Uygulama,
   FlyWire/Codex konektomunun bir alt kümesiyle gelir: 5.958 Mantar
   Cisimciği nöronu (685 ALPN girdi, 5.177 Kenyon hücresi aktarıcı, 96 MBON
   çıktı) ve 79.423 sinaptik bağlantı.
2. **Sinyali iki kez gönderir.** Sinyal bir kez sağlıklı ağda, bir kez de
   hasarlı kopyada yayılır; her çıktı nöronunun ne zaman ateşlendiği
   kaydedilir.
3. **Alzheimer benzeri hasar uygular.** Hasarı **Bozulmalar** panelinden
   siz seçersiniz. *Tau* ve *Beta-Amiloid* iletimi yavaşlatır; *GABA* ve
   *APL* ateşleme eşiğini yükseltir. Her birinin %0–100 arası kendi şiddeti
   vardır ve birden fazlasını üst üste ekleyebilirsiniz.
4. **Sonucu ölçer.** Milisaniye cinsinden ek gecikmeyi, çıktı nöronu başına
   % sapmayı, Weber-Fechner zaman algısı tahminini ve iki ağın yan yana
   canlandırılmış oynatımını gösterir.

Hasar eğrileri, ms kalibrasyonu ve algı modeli, literatür veya laboratuvar
değerleri gelene kadar **yer tutucudur**. Sayılar modelin nasıl davrandığını
gösterir; klinik bir tahmin değildir.

### Hızlı başlangıç

- **Sadece kullanmak için:** [mb-delay-sim.streamlit.app](https://mb-delay-sim.streamlit.app/?embed=true) adresini
  açın. Gerçek konektom varsayılan olarak yüklenir; kenar çubuğunun en
  üstünden dili Türkçe yapabilirsiniz.
- **Test etmek için:** [8. bölümdeki](#8-nasıl-test-edilir) kontrol listesini
  izleyin.
- **Yerelde çalıştırmak veya geliştirmek için:** aşağıdaki Kurulum
  bölümüne bakın.

### 1. Kurulum (yalnızca yerel geliştirme için)

```
git clone https://github.com/dieudonneiot/mushroom-body-delay-sim.git
cd mushroom-body-delay-sim
python -m venv .venv
.venv/Scripts/activate   # macOS/Linux'ta .venv/bin/activate
pip install -e ".[dev]"
```

Python 3.10+ gerektirir. Depo herkese açıktır (public), herkes klonlayabilir.
Yerel kurulum yalnızca kodu değiştirmek veya testleri çalıştırmak için
gereklidir; uygulamayı kullanmak için yukarıdaki canlı bağlantıyı açmanız
yeterlidir.

Bu komut `mbsim` paketini ve `streamlit`, `plotly`, `networkx`, `pandas`,
`matplotlib`, `pyyaml` ile (`[dev]` sayesinde) `pytest`'i kurar.

Proje klasörünü `.venv` zaten oluşturulduktan sonra taşır veya yeniden
adlandırırsanız, `.venv`'i silip yeniden oluşturun (`rm -rf .venv`, ardından
yukarıdaki iki komutu tekrar çalıştırın) — venv'in `pip`/`streamlit` gibi
başlatıcıları oluşturulma anındaki mutlak yolu sabit olarak içine gömer ve o
yol artık yoksa sessizce bozulur ("Fatal error in launcher").

### 2. Gerçek konektom verisini edinme

Codex genel/toplu bir API sunmuyor — veri, elle CSV olarak dışa aktarılır.
https://codex.flywire.ai adresinden giriş yapın, üst çubuktaki **Downloadable
assets** (indirme simgesi) bölümüne gidin, `FAFB` veri setini seçin ve tam
olarak şu iki dosyayı indirin:

- **"Connections (Filtered)"** → `data/raw/connections.csv` olarak kaydedin
- **"Classification / Hierarchical Annotations"** → `data/raw/classification.csv` olarak kaydedin

Sayfadaki diğer her şeyi atlayın — "Synapse Table" ve "Neuron Skeletons"
birkaç gigabayt boyutundadır ve bu işlem hattı ikisini de hiçbir zaman okumaz.
Ayrıntılar (bir şema tuzağı dahil) [data/raw/README.md](data/raw/README.md)
dosyasında; kısacası: gerçek Codex dışa aktarımında **`cell_type` sütunu
yoktur** — bunun yerine `class` sütunu vardır, değerleri: `ALPN` (girdi,
örnek verideki `PN`'ye karşılık gelir), `Kenyon_Cell` (aktarıcı, `KC`'ye
karşılık gelir), `MBON` (çıktı), isterseniz düzenleyici dopaminerjik yolağı
da eklemek için `DAN`/`MBIN`. `mbsim.io`, `class` sütununu otomatik olarak
`cell_type` olarak eşler, bu yüzden CSV'yi elle düzenlemenize gerek yoktur —
gerçek etiket adlarını yalnızca yolak rollerini seçerken (arayüzde veya bir
yapılandırma dosyasında) bilmeniz yeterlidir.

Her iki dosya da yerine konduktan sonra, ya `configs/default.yaml` dosyasını
düzenleyin (`data.mode: raw` yapın ve `roles`'u gerçek etiketlerle güncelleyin)
ya da doğrudan hazır [configs/raw.yaml](configs/raw.yaml) dosyasını kullanın —
ikisi de zaten ayarlanmıştır, aşağıdaki "CLI" bölümüne bakın.

Uygulamayı kullanmak için bu adıma gerek yoktur. Gerçek veriden hazırlanmış
bir alt küme zaten `data/connectome/` içindedir ve varsayılan olarak yüklenir
(bkz. [data/connectome/README.md](data/connectome/README.md)); `data/fixtures/`
içindeki küçük sentetik grafik (3 PN, 6 KC, 2 MBON nöronu, tamamen bağlı) da
hızlı kontroller için her zaman kullanılabilir.

### 3. Etkileşimli Arayüz

Uygulama Streamlit Community Cloud üzerinde
[mb-delay-sim.streamlit.app](https://mb-delay-sim.streamlit.app/?embed=true) adresinde yayındadır ve `main` dalına
yapılan her push'ta kendiliğinden yeniden dağıtılır. Yerelde çalıştırmak
için:

```
streamlit run app.py
```

Ekrandaki her şeyin ayrıntısı:

**Dil seçici (Language toggle)** — kenar çubuğunun en üstünde, **English** ve
**Türkçe** arasında bir geçiş anahtarı. Her etiketi, düğmeyi, sekmeyi, uyarıyı,
grafik başlığını ve hatta grafik üzerindeki ipucu (hover tooltip) metinlerini
yeniden çevirir — hiçbir şey diğer dilde kalmaz. İstediğiniz zaman
değiştirebilirsiniz; diğer ayarlarınız (kaydırıcılar, veri kaynağı) korunur.

**Kenar çubuğu — Veri kaynağı**
- *Dahil edilen konektom (Princeton dışa aktarımı)* — `data/connectome/` içindeki gerçek veriden hazırlanmış ALPN/Kenyon_Cell/MBON alt kümesi; varsayılan olarak açılır ve Community Cloud uygulamasına dahildir.
- *Örnek veri (demo)* — `data/fixtures/` içindeki küçük sentetik grafik; hızlı bir demo için her zaman kullanılabilir.
- *data/raw/ (yerel dosyalar)* — yalnızca `data/raw/` içinde her iki CSV de varsa gösterilir; tam dışa aktarımı yerel geliştirmede kullanmak içindir.
- *CSV yükle* — iki dosya yükleme alanı belirir; kendi `connections.csv` ve `classification.csv` dosyalarınızı bilgisayarınızdan doğrudan sürükleyip bırakabilirsiniz (proje klasörüne koymanıza gerek yoktur). Farklı bir Codex veri sürümünü veya birinin size e-posta ile gönderdiği bir alt kümeyi denemek için kullanışlıdır.

**Kenar çubuğu — Mantar Cisimciği yolağı**
Veri yüklendikten sonra, verinizde bulunan her farklı `cell_type` değeriyle
önceden doldurulmuş üç açılır (çoklu seçim) menü belirir:
- *Girdi hücre tipi/tipleri* — sinyalin başladığı nöron tipleri (varsayılan olarak `PN`, varsa).
- *Aktarıcı (relay) hücre tipi/tipleri* — sinyalin geçtiği ara katman (varsayılan olarak `KC`).
- *Çıktı hücre tipi/tipleri* — sinyal varış zamanının ölçüldüğü yer (varsayılan olarak `MBON`).

Her rol için birden fazla tip seçebilirsiniz (örn. birden çok girdi tipi) ve
veri setiniz farklı etiketler kullanıyorsa bunları serbestçe değiştirebilirsiniz
— hiçbir şey PN/KC/MBON'a sabitlenmemiştir, bunlar yalnızca mevcut olduklarında
kullanılan varsayılan değerlerdir.

**Kenar çubuğu — Simülasyon parametreleri** (hepsi anlık olarak günceller, tıklanacak bir düğme yoktur)
- *Sağlıklı iletim hızı* (0.1–3.0, varsayılan 1.0) — hasarsız ağdaki temel sinyal hızı. Daha yüksek = daha hızlı sinyal.
- *Ateşleme eşiği* (0.5–5.0, varsayılan 1.0) — bir nöronun "ateşlenip" sinyali ileriye iletmesi için ne kadar birikmiş girdi sinyaline ihtiyacı olduğu.
**Kenar çubuğu — Bozulmalar** (Alzheimer hasarı kontrolleri)
- Bir hasar satırı eklemek için **＋ Bozulma Ekle**'ye tıklayın. *Bozulma tipi*ni seçin ve *Şiddet (%)* değerini 0–100 arasında kaydırıcıyla veya sayı kutusuyla ayarlayın. Satırlar üst üste eklenir; **✕** düğmesi bir satırı kaldırır.
  - *Tau Proteini* ve *Beta-Amiloid*, hedefledikleri bağlantılarda iletim hızını düşürür.
  - *GABA İşlev Bozukluğu* ve *APL Nöron Bozulması*, hedefledikleri nöronlarda ateşleme eşiğini yükseltir. APL'nin etkili olması için alanına bir root_id girilmesi gerekir; girilmezse etkisi olmaz.
- Hiç satır yoksa sağlıklı ve hasarlı ağ aynıdır; bu durumda %0 sapma beklenen sonuçtur.
- Sekmelerin üstündeki açıklamalar, her kanalın kaç bağlantıyı ve nöronu etkilediğini ve ortalama şiddeti gösterir.
- Şiddetler `mbsim/damage.py` içindeki yer tutucu doğrusal eğrilerden geçer; aşağıdaki "Gerçek bir hasar modeliyle genişletme" bölümüne bakın.
- *Kalibrasyon (yer tutucu)* paneli: simüle edilmiş zaman birimi başına milisaniye; ms cinsinden gösterilen değerlerde kullanılır.

**Ana alan — "Algı ve Gecikme" sekmesi** (ilk açılan sekme)
- *Fiziksel İletim Gecikmesi*: ortalama sağlıklı gecikme, ortalama hasarlı gecikme ve aradaki net fark (Δ), hepsi ms cinsinden.
- *Weber-Fechner Zaman Algısı Sapması*: sağlıklı ve hasarlı için algılanan-fiziksel zaman eğrileri ve % sapma. Yer tutucu bir model kullanır (`mbsim/perception.py`).
- *Deneme-tabanlı Weber kesri tahmini* paneli: **▶ Denemeleri çalıştır**'a tıklayınca N gürültülü deneme çalıştırır (bkz. 6. bölüm).

**Ana alan — "Ağ Görünümü" sekmesi**
- Üstte beş KPI kartı: ortalama ve medyan % gecikme sapması, hedeflenen bağlantı ve nöronlardaki ortalama hasarlı iletim hızı ile ortalama hasarlı ateşleme eşiği (o kanal kullanılmıyorsa `n/a` görünür) ve sinyalin toplam çıktı nöronundan kaçına ulaştığı.
- Soldan sağa (girdi → aktarıcı → çıktı) düzenlenmiş bir **gecikme farkı** ağ grafiği. Her nöron, hasarlı ağda sağlıklı ağa göre ne kadar geç (kırmızı) veya erken (mavi) ateşlendiğine göre renklendirilir. **Bir nöronun üzerine gelerek** kimliğini, rolünü, gelen/giden bağlantı sayısını ve varış zamanlarını görebilirsiniz. **Yakınlaştırmak ve kaydırmak için kaydırın veya sürükleyin.**
- Daraltılabilir "Mutlak varış zamanlarını göster" paneli, sağlıklı ve hasarlı grafikleri ortak bir renk skalasında, varış zamanına göre renklendirilmiş olarak yan yana gösterir. Gri nöronlara sinyal hiç ulaşmamıştır.
- Daraltılabilir "Yolak yapısını göster" paneli aynı grafiği role göre renklendirir; böylece simülasyon katmanı olmadan bağlantı yapısını inceleyebilirsiniz.
- Nokta boyutu, nöron etiketleri ve kenar (edge) opaklığı büyük grafiklerde (gerçek konektom ölçeğinde: binlerce nöron, on binlerce bağlantı) otomatik olarak küçülür/azalır; böylece görünüm bir yapılandırma gerekmeden okunaklı kalır, katı bir bulanıklığa dönüşmez.

**Ana alan — "Karşılaştırma" sekmesi**
Gruplandırılmış bir çubuk grafik: her çıktı nöronu için sağlıklı ve hasarlı
varış zamanı bir çift çubuk olarak gösterilir. Bu, "Veri" sekmesindeki CSV ile
aynı sayıların grafik biçimidir.

**Ana alan — "Veri" sekmesi**
Ham karşılaştırma tablosu (ulaşılan her çıktı nöronu için bir satır: sağlıklı
zaman, hasarlı zaman, % sapma), seçtiğiniz dile çevrilmiş sütun başlıkları,
ve bunu yerel olarak kaydetmek (indirilen dosyada başka yerlerde tekrar
işlenebilmesi için sabit İngilizce sütun adlarıyla) veya tıp ekibiyle
paylaşmak için bir "comparison.csv dosyasını indir" düğmesi.

**Ana alan — "Canlı Yayılım" sekmesi**
Sinyalin sağlıklı ve hasarlı ağlarda ortak bir simüle-zaman ekseninde nasıl
yayıldığını gösteren, canlandırılmış, yan yana bir oynatım. Grafiğin sol
üstündeki **▶ Oynat** düğmesine basarak nöronların — ateşlendikleri anda role
göre renklendirilmiş olarak — yandığını izleyin, ya da elle belirli bir ana
gitmek için grafiğin altındaki kaydırıcıyı sürükleyin. Grafiklerin üstündeki
canlı okuma (`t = ... | Sağlıklıda ateşlenen: X/Y | Hasarlıda ateşlenen: X/Y`)
hasarlı ağın gecikmesini ince bir görsel farktan ziyade tam bir sayı olarak okunaklı kılar;
dikey bir ayırıcı çizgi de iki ayrı ağın yan yana gösterildiğini açıkça
belirtir. Kareler zamanda doğrusal değil, *ateşlenme zamanının yüzdelik
dilimine (quantile)* göre aralıklandırılır: gerçek ateşlenme zamanı
dağılımları oldukça öne yüklüdür (ağın çoğu neredeyse anında ateşlenir,
ardından uzun bir "gecikmiş nöronlar" kuyruğu gelir), bu yüzden yüzdelik dilim
aralıklandırması her karenin benzer sayıda yeni etkinleşmiş nöron göstermesini
sağlar — bir parlama ve ardından onlarca neredeyse durağan kareden ziyade
düzgün, eşit tempolu bir dalga. Bir **"Oynatma hızı"** kaydırıcısı (kare
başına 50–1500 ms, varsayılan 400 ms — yüksek değer daha yavaş demektir) tam
olarak neler olduğuna daha yakından bakmak için yavaşlatmanızı sağlar.

**Hata yönetimi** — rol seçiminiz hiçbir nöronla eşleşmiyorsa, bir CSV
dosyasında beklenen bir sütun eksikse veya sinyal hiçbir çıktı nöronuna
ulaşmıyorsa, bir hata yerine (seçtiğiniz dilde) sade bir mesaj görürsünüz.

### 4. CLI (toplu/batch mod)

```
python -m mbsim.cli --config configs/default.yaml
```

Çıkarılan alt-grafik için bir sağlık kontrolü (sanity report) raporu, ardından
çıktı nöronlarında sağlıklı ve hasarlı sinyal gecikmesi karşılaştırmasını
yazdırır ve `outputs/comparison.csv`, `outputs/comparison.png`,
`outputs/network_structure.png`, `outputs/network_healthy.png`,
`outputs/network_damaged.png` dosyalarını (statik matplotlib görselleri — bir
rapor/e-posta için kullanışlı; canlı keşif için ise Streamlit uygulamasını
kullanın) oluşturur.

Gerçek konektom `data/raw/` içine konduktan sonra (yukarıdaki 2. adıma bakın),
bunun yerine hazır [configs/raw.yaml](configs/raw.yaml) dosyasını kullanın —
`default.yaml` ile aynıdır, yalnızca `data.mode: raw` ve `roles` zaten gerçek
`ALPN`/`Kenyon_Cell`/`MBON` etiketleriyle ayarlanmıştır:

```
python -m mbsim.cli --config configs/raw.yaml
```

Gerçek konektom ölçeğinde matplotlib çizici, hem hız hem de okunabilirlik için
kenarları (edge) otomatik olarak inceltir, noktaları küçültür, kenar oku
başlarını ve nöron etiketlerini kaldırır (bkz. `mbsim/layout.py`) — tam FAFB
Mantar Cisimciği alt-grafiğinde (~6.000 nöron, ~79.000 bağlantı) tüm CLI
çalıştırması bir dakikanın çok altında tamamlanır.

Koda dokunmadan değiştirmek için `configs/default.yaml` dosyasını (veya
`configs/raw.yaml` gibi kendi kopyanızı) düzenleyin:
- `data.mode`: `fixture` veya `raw`
- `roles`: hangi hücre tiplerinin girdi/aktarıcı/çıktı sayılacağı — örnek veri
  için `PN`/`KC`/`MBON`, gerçek Codex verisi için `ALPN`/`Kenyon_Cell`/`MBON`
- `simulation.conduction_velocity`, `simulation.threshold`
- `damage.perturbations`: uygulamanın "＋ Bozulma Ekle" panelindeki ile aynı Tau/Amiloid/GABA/APL yığını (biçim için `configs/default.yaml` dosyasına bakın)
- `output.dir`: sonuçların yazılacağı yer

### 5. Gerçek bir hasar modeliyle genişletme

Her bozulma (Tau, Amiloid, GABA, APL), herhangi bir hasar uygulanmadan önce
gerçekten etkileyebileceği *belirli* bağlantılara/nöronlara çözümlenir —
hangi konektom alanının kullanıldığı için `src/mbsim/targeting.py`'nin modül
docstring'ine bakın (Tau/Amiloid varsayılan olarak her bağlantıyı hedefler;
GABA, gerçek Codex `nt_type` değeri `"GABA"` olan bağlantıları hedefler;
APL'nin hiçbir varsayılanı yoktur, çünkü sınıflandırma dışa aktarımında ayrı
bir etiketi yoktur — codex.flywire.ai'de ada göre aratıp bulduğunuz bir
root_id'yi `target_root_ids` ile hedefleyin). Bundan iki bağımsız kanal
çıkar: bağlantı başına iletim hızı şiddeti ve nöron başına ateşleme eşiği
şiddeti (bkz. `src/mbsim/perturbations.py`).

`src/mbsim/damage.py` içinde bu şiddetleri gerçek sayılara dönüştüren iki
yer tutucu eğri bulunur: `linear_slowdown` (hız azalması) ve
`linear_threshold_increase` (eşik artışı), ikisi de [0, 1] aralığında
doğrusaldır. Tıp ekibi literatüre dayalı fonksiyonlar sağladığında (şiddet ->
azalma), bunları oraya yazın ve `mbsim.metrics.compare(...)` fonksiyonuna
`slowdown_fn`/`threshold_fn` olarak geçirin (hem `app.py` hem de `cli.py`'de
zaten bağlanmıştır) — işlem hattının başka hiçbir yerinde değişiklik gerekmez.

`src/mbsim/calibration.py`, simülasyonun soyut zaman birimlerini
milisaniyeye çeviren tek yer tutucu sabiti barındırır — gerçek zamanlama
verisi (Faz 2 laboratuvar ölçümleri veya bir literatür değeri) elde
edildiğinde bu fonksiyonun gövdesini değiştirin.

### 6. Deneme-tabanlı Weber kesri tahmini

Tek bir sağlıklı-hasarlı karşılaştırması bir nokta tahminidir, bir Weber
kesrinin asıl ölçtüğü denemeler-arası değişkenlik değildir.
`src/mbsim/trials.py`'nin `compare_trials` fonksiyonu her taraf için N
bağımsız gürültülü deneme çalıştırır (iletim hızında yer tutucu log-normal
gürültü — bkz. modül docstring'i) ve her durum için değişim katsayısını
(std/ortalama varış zamanı) ampirik bir Weber-kesri-benzeri sayı olarak
bildirir. Uygulamada, Algı sekmesindeki "Deneme-tabanlı Weber kesri tahmini"
panelini açın ve "▶ Denemeleri çalıştır"a tıklayın (gerçek konektomda
~10-15 saniye sürdüğünden bir düğmenin arkasına gizlenmiştir).

### 7. Faz 2/3 verisi elde edildiğinde doğrulama

`src/mbsim/validation.py`, simülasyonun % sapmasını Faz 2 sinek tırmanma
deneyi % sapmasıyla ve/veya Faz 3 insan zaman algısı görevi sapmasıyla
karşılaştırır ve her ampirik kaynağın simülasyonla *aynı yönde* hareket edip
etmediğini bildirir — projenin asıl doğrulama hedefi budur (bkz. modülün
docstring'i), tam bir yüzde eşleşmesi değil. Her iki veri kaynağı da henüz
mevcut değil; `data/lab/README.md` ve `data/clinical/README.md`, bu veriyi
ileride dışa aktaracak kişinin formatı bilmesi için beklenen CSV şeklini
(boş `.template.csv` dosyalarıyla birlikte) belgeler, ve `validation.py`'nin
kendi testleri karşılaştırma mantığını şimdiden aynı şekilde biçimlendirilmiş
sentetik veriyle çalıştırır.

Bu karşılaştırma uygulamanın kendisinde de sunulur — **"Faz 2/3 Doğrulama"**
sekmesi, bir tırmanma-deneyi CSV'si ve/veya bir zaman-algısı-görevi CSV'si
(herhangi biri mevcut olduğunda) yüklemenize ve simülasyonun % sapmasının bu
verilerle yan yana karşılaştırmasını, her biri için bir "aynı yön" kontrolüyle
birlikte görmenize olanak tanır. Her iki veri kaynağı da henüz mevcut
olmadığından, bir **"▶ Sentetik örnek veriyi yükle"** düğmesi bunun yerine
açıkça etiketlenmiş bir yer tutucu veri seti yükler; böylece karşılaştırma
mekanizmasının kendisi, gerçek veri elde edilmeden önce (örn. bir sunum için)
gösterilebilir.

### 8. Nasıl test edilir

#### A. Tarayıcıda (kurulum yok, ~5 dakika)

[mb-delay-sim.streamlit.app](https://mb-delay-sim.streamlit.app/?embed=true) adresini açın. Bir "wake up" düğmesi
görürseniz ücretsiz uygulama uykudadır; tıklayın ve yaklaşık 30 saniye
bekleyin. Ardından her adımı beklenen sonuçla karşılaştırın. Değerler,
varsayılan veri kaynağıyla (*Dahil edilen konektom (Princeton dışa
aktarımı)*) canlı uygulamadan alınmıştır.

| # | Yapılacak | Beklenen sonuç |
|---|---|---|
| 1 | Başlığın altındaki açıklamaya bakın | `Grafik: 5958 nöron, 79423 sinaptik bağlantı (aktarıcı: 5177, çıktı: 96, girdi: 685)` |
| 2 | Kenar çubuğunda dili **English** yapın, sonra geri **Türkçe** yapın | Tüm etiketler, sekmeler ve grafik başlıkları dil değiştirir; ayarlarınız korunur |
| 3 | Bozulma eklemeden **Algı ve Gecikme** sekmesine bakın | Sağlıklı ve hasarlı gecikme ikisi de **0.34 ms**, sapma **%0**; mavi bir not %0'ın beklenen sonuç olduğunu açıklar |
| 4 | **＋ Bozulma Ekle**'ye tıklayın, *Tau Proteini* kalsın, şiddet kutusuna **40** yazın | Açıklama: `79423/79423 bağlantı etkilendi (ortalama şiddet %40.0)`. Gecikme **0.34 → 0.57 ms (+0.23)**, zaman algısı sapması **%66.7** olur |
| 5 | *Deneme-tabanlı Weber kesri* panelini açıp **▶ Denemeleri çalıştır**'a tıklayın | Birkaç saniye sonra sağlıklı ve hasarlı Weber kesirleri görünür (varsayılanlarla her biri yaklaşık %6) |
| 6 | **Ağ Görünümü** sekmesi | KPI'lar: ortalama ve medyan sapma **%66.7**, hasarlı hız **0.600**, eşik `n/a`, ulaşılan çıktı **96/96**. Grafikte kırmızı (gecikmiş) Kenyon hücreleri görünür |
| 7 | **Karşılaştırma** sekmesi | Her çıktı nöronu için yan yana sağlıklı ve hasarlı çubuklar; hasarlı çubuk her yerde daha yüksek |
| 8 | **Veri** sekmesinde **comparison.csv dosyasını indir**'e tıklayın | 96 satır, her birinde `% sapma` ≈ 66.67; bir CSV dosyası iner |
| 9 | **Canlı Yayılım** sekmesinde **▶ Oynat**'a basın veya kaydırıcıyı ortaya sürükleyin | t ≈ 0.056'da okuma, sağlıklı ağda yaklaşık **4380/5958**, hasarlı ağda **1889/5958** ateşlenmiş nöron gösterir |
| 10 | **Faz 2/3 Doğrulama** sekmesinde **▶ Sentetik örnek veriyi yükle**'ye tıklayın | Simülasyon %66.7, sinek %30.0 ve insan %30.0; ikisi de **✅ Evet** (aynı yön) |
| 11 | İkinci bir bozulma ekleyin: **GABA İşlev Bozukluğu**, %50 (Tau %40'ta kalsın) | Açıklama: `295/5958 nöron etkilendi (ortalama şiddet %50.0)`. *Hasarlı ateşleme eşiği* **1.500** olur; ortalama ve medyan sapma **%175.2** ve **%170.2**'ye çıkar |
| 12 | Tau şiddetini **100** yapın | Bir uyarı, iletimin neredeyse tamamen durması nedeniyle sayıların tasarım gereği aşırı görüneceğini açıklar. %100 Tau'da iletim durduğu için "sinyal hiçbir çıktı nöronuna ulaşmadı" mesajı da beklenen bir sonuçtur |
| 13 | Veri kaynağı → **Örnek veri (demo)** | `Grafik: 11 nöron, 13 sinaptik bağlantı (girdi: 3, aktarıcı: 6, çıktı: 2)`; roller varsayılan olarak PN/KC/MBON olur |

#### B. Otomatik testler (yerel)

```
pip install -e ".[dev]"
pytest
```

Tüm testler `data/fixtures/` içindeki sentetik veriye karşı çalışır; gerçek
Codex indirmesine ihtiyaç duymazlar.

#### C. Toplu CLI (yerel)

```
python -m mbsim.cli --config configs/default.yaml
```

Bu komut örnek veri üzerinde %30 Tau bozulmasıyla çalışır, karşılaştırmayı
yazdırır ve `outputs/` altına beş dosya yazar. Dahil edilen gerçek alt küme
üzerinde çalıştırmak için `configs/raw.yaml` dosyasını kopyalayıp
`raw_dir: data/connectome` yapın.

Bunlardan herhangi biri burada anlatılanla uyuşmuyorsa, önce beklenen
sütunlar ve dosya adları için `data/connectome/README.md` veya
`data/raw/README.md` dosyasına bakın.

### Proje yapısı

```
app.py                    # Streamlit etkileşimli arayüz
src/mbsim/
  io.py                   # Codex CSV dışa aktarımlarını yükler + doğrular
  mushroom_body.py         # yapılandırılan girdi/aktarıcı/çıktı yolağına göre filtreler
  graph.py                 # NetworkX grafik oluşturma + sağlık kontrolleri
  simulation.py            # olay-tabanlı sinyal yayılımı
  targeting.py              # her bozulmayı etkilediği belirli bağlantılara/nöronlara çözümler
  perturbations.py          # adlandırılmış bozulmalar (Tau/Amiloid/GABA/APL) -> bağlantı/nöron başına şiddet
  damage.py                 # şiddet -> iletim hızı yavaşlaması / ateşleme eşiği artışı (değiştirilebilir)
  calibration.py             # simüle edilmiş zaman birimleri -> milisaniye (değiştirilebilir)
  metrics.py                # sağlıklı/hasarlı karşılaştırma + % sapma
  trials.py                  # Monte Carlo denemeler-arası değişkenlik -> ampirik Weber kesri
  validation.py               # simülasyon çıktısını Faz 2/3 ampirik verisiyle karşılaştırır
  layout.py                  # ortak nöron yerleşimi / rol renkleri / büyük grafik ölçekleme
  visualize.py                # statik matplotlib grafikleri (CLI tarafından kullanılır)
  plotly_viz.py                 # etkileşimli Plotly grafikleri + yayılım animasyonu (uygulama tarafından kullanılır)
  i18n.py                        # İngilizce/Türkçe arayüz metni çevirileri
  inference.py                   # Faz A ters çıkarım (ABC + simülasyon tabanlı kalibrasyon), henüz arayüzde değil
  cli.py                          # toplu (batch) giriş noktası
scripts/prepare_connectome.py  # data/connectome/ klasörünü ham Codex dışa aktarımlarından oluşturur
configs/default.yaml       # CLI yapılandırması (örnek veri, PN/KC/MBON rolleri)
configs/raw.yaml           # gerçek veri için CLI yapılandırması (ALPN/Kenyon_Cell/MBON rolleri)
data/fixtures/             # sentetik demo verisi (git'te izlenir)
data/connectome/           # uygulamayla dağıtılan Princeton konektom alt kümesi (git'te izlenir)
data/raw/                  # kaynak Codex dışa aktarımları / yerel tam veri (gitignore'da)
data/lab/                  # Faz 2 sinek deneyi sonuçları, toplandığında buraya (gitignore'da)
data/clinical/             # Faz 3 insan görev sonuçları, toplandığında buraya (gitignore'da)
tests/                     # pytest test paketi
```
