# Mushroom Body Signal-Delay Simulation

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
| **Conduction velocity** | How fast a signal travels along a connection; the simulation's speed parameter, reduced by disease severity. | Bir sinyalin bağlantı boyunca ne kadar hızlı ilerlediği; hastalık şiddetiyle azaltılan simülasyon hız parametresi. |
| **Firing threshold** | The amount of accumulated incoming signal a neuron needs before it "fires" and forwards the signal onward. | Bir nöronun "ateşlenip" sinyali sonraki nöronlara iletmesi için ihtiyaç duyduğu birikmiş gelen sinyal miktarı. |
| **Disease severity** | The simulation's single knob for how much Alzheimer's-like damage is applied (0 = none, 1 = maximum); currently mapped through a placeholder linear function. | Simülasyonun, ne kadar Alzheimer benzeri hasar uygulanacağını belirleyen tek kadranı (0 = yok, 1 = maksimum); şu anda yer tutucu bir doğrusal fonksiyon üzerinden hesaplanır. |
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

### 1. Setup

```
git clone https://github.com/dieudonneiot/mushroom-body-delay-sim.git
cd mushroom-body-delay-sim
python -m venv .venv
.venv/Scripts/activate   # .venv/bin/activate on macOS/Linux
pip install -e ".[dev]"
```

Requires Python 3.10+. The repo is currently **private** — ask to be added as
a GitHub collaborator before cloning if you don't already have access.

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

Until real data is in place, everything runs against the small synthetic
graph in `data/fixtures/` (3 PN, 6 KC, 2 MBON neurons, fully wired) so you can
try every feature immediately with no setup.

### 3. Interactive UI (recommended)

```
streamlit run app.py
```

**One-command launch:** `.\sirin.ps1` (PowerShell) or `./sirin.sh` (Git Bash/WSL/macOS/Linux) —
or just double-click `sirin.bat` on Windows. This first pulls the latest `main`
and installs/updates dependencies, then starts the app — all best-effort: if
there's no network or git credentials aren't cached, it prints a one-line
warning and launches anyway with whatever code is already on disk, so it
never hangs or blocks (safe to run right before a live demo).

This opens a browser tab. Every detail of what's on screen:

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
- *Disease severity* (0.0–1.0, default 0.3) — the Alzheimer's-damage knob. 0 = no damage (identical to healthy), 1 = maximum slowdown. This currently maps through a placeholder linear function (`mbsim/damage.py`); swap in a literature-derived one when the medical team provides it (see "Extending the damage model" below).

**Main area — "Network View" tab**
- Four KPI cards at the top: mean % delay deviation, median % delay deviation, the damaged conduction velocity actually used (derived from the severity slider), and how many output neurons the signal reached out of the total configured.
- Two side-by-side **interactive** network graphs — "Healthy network" and "Damaged network" — built from the same NetworkX graph, laid out left-to-right (input → relay → output). Node color = signal arrival time (a shared color scale across both graphs so the comparison is visually fair); gray nodes were never reached by the signal. **Hover over any neuron** to see its id, role, in-degree, out-degree, and (if reached) exact arrival time. **Scroll/drag to zoom and pan** — useful once you load the real connectome with hundreds of Kenyon cells.
- A collapsible "Show pathway structure" panel below — the same interactive graph, but colored by role (input/relay/output) instead of arrival time, so you can inspect the wiring itself without any simulation overlay.
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

### 8. Tests & verifying everything end-to-end

Automated:

```
pytest
```

All tests run against the synthetic fixture in `data/fixtures/`, so they don't
require the real Codex download.

To manually verify the full pipeline yourself, in order:

1. `streamlit run app.py` with the default **Fixture (demo data)** source
   selected — confirms the UI, both languages, and all four tabs work with
   zero setup.
2. Get the real data into `data/raw/` (step 2 above), then in the app switch
   **Data source** to **data/raw/ (local files)** — the pathway dropdowns
   should auto-populate with real labels like `ALPN`, `Kenyon_Cell`, `MBON`,
   `DAN`. Check the KPI card "Output neurons reached" — for the full FAFB
   Mushroom Body pathway at default parameters this should read 96/96.
3. `python -m mbsim.cli --config configs/raw.yaml` — should finish in well
   under a minute and print the same reached-count in its summary, plus write
   all five files under `outputs/`.
4. Open the "Live Propagation" tab, press **▶ Play**, and confirm the damaged
   panel's fired-count visibly trails the healthy panel's mid-animation (with
   default parameters on the real dataset, the gap is largest around
   t≈0.04–0.08 — e.g. roughly 3300 vs. 1500 nodes fired at the same instant).

If any of these disagree with what's described here, something in your local
data or config differs from what this README assumes — check
`data/raw/README.md` for the exact expected columns and file names first.

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
  cli.py                  # batch entrypoint
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

### 1. Kurulum

```
git clone https://github.com/dieudonneiot/mushroom-body-delay-sim.git
cd mushroom-body-delay-sim
python -m venv .venv
.venv/Scripts/activate   # macOS/Linux'ta .venv/bin/activate
pip install -e ".[dev]"
```

Python 3.10+ gerektirir. Depo şu anda **özel (private)** — erişiminiz yoksa
klonlamadan önce GitHub üzerinde işbirlikçi (collaborator) olarak
eklenmenizi isteyin.

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

Gerçek veri yerine konana kadar her şey `data/fixtures/` içindeki küçük
sentetik grafik (3 PN, 6 KC, 2 MBON nöronu, tamamen bağlı) üzerinde çalışır;
böylece hiçbir kurulum yapmadan tüm özellikleri hemen deneyebilirsiniz.

### 3. Etkileşimli Arayüz (önerilen)

```
streamlit run app.py
```

**Tek komutla başlatma:** `.\sirin.ps1` (PowerShell) veya `./sirin.sh` (Git
Bash/WSL/macOS/Linux) — Windows'ta `sirin.bat` dosyasına çift tıklamak da
yeterli. Bu, önce en güncel `main` dalını çeker ve bağımlılıkları
kurar/günceller, ardından uygulamayı başlatır — hepsi "elden geldiğince":
ağ yoksa veya git kimlik bilgileri önbelleğe alınmamışsa, tek satırlık bir
uyarı yazdırıp yine de eldeki koduyla başlatmaya devam eder; bu yüzden asla
takılıp kalmaz veya engellenmez (canlı bir sunumdan hemen önce çalıştırmak
güvenlidir).

Bu komut tarayıcıda bir sekme açar. Ekrandaki her şeyin ayrıntısı:

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
- *Hastalık şiddeti* (0.0–1.0, varsayılan 0.3) — Alzheimer hasarı kadranı. 0 = hasar yok (sağlıklı ile aynı), 1 = maksimum yavaşlama. Şu anda yer tutucu (placeholder) doğrusal bir fonksiyon (`mbsim/damage.py`) üzerinden hesaplanır; tıp ekibi literatüre dayalı bir fonksiyon sağladığında bunu değiştirebilirsiniz (aşağıdaki "Gerçek hasar modeliyle genişletme" bölümüne bakın).

**Ana alan — "Ağ Görünümü" sekmesi**
- Üstte dört KPI kartı: ortalama % gecikme sapması, medyan % gecikme sapması, gerçekte kullanılan hasarlı iletim hızı (hastalık şiddeti kaydırıcısından türetilir) ve sinyalin, yapılandırılan toplam çıktı nöronundan kaçına ulaştığı.
- Yan yana iki **etkileşimli** ağ grafiği — "Sağlıklı ağ" ve "Hasarlı ağ" — aynı NetworkX grafiğinden oluşturulmuş, soldan sağa (girdi → aktarıcı → çıktı) düzenlenmiştir. Nöron rengi = sinyal varış zamanı (karşılaştırmanın görsel olarak adil olması için her iki grafikte de ortak bir renk skalası kullanılır); gri nöronlara sinyal hiç ulaşmamıştır. **Herhangi bir nöronun üzerine gelerek** kimliğini, rolünü, gelen/giden bağlantı sayısını ve (ulaşıldıysa) tam varış zamanını görebilirsiniz. **Yakınlaştırmak ve kaydırmak için kaydırın/sürükleyin** — gerçek konektomu yüzlerce Kenyon hücresiyle yüklediğinizde faydalıdır.
- Altta daraltılabilir bir "Yolak yapısını göster" paneli — aynı etkileşimli grafik, ancak varış zamanı yerine role göre (girdi/aktarıcı/çıktı) renklendirilmiştir; böylece herhangi bir simülasyon katmanı olmadan bağlantı yapısını inceleyebilirsiniz.
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

### 8. Testler ve her şeyi uçtan uca doğrulama

Otomatik:

```
pytest
```

Tüm testler `data/fixtures/` içindeki sentetik veriye karşı çalışır; bu yüzden
gerçek Codex indirmesine ihtiyaç duymazlar.

Tüm işlem hattını elle doğrulamak için, sırasıyla:

1. Varsayılan **Örnek veri (demo)** kaynağı seçiliyken `streamlit run app.py`
   çalıştırın — arayüzün, her iki dilin ve dört sekmenin tamamının hiçbir
   kurulum yapmadan çalıştığını doğrular.
2. Gerçek veriyi `data/raw/` içine koyun (yukarıdaki 2. adım), ardından
   uygulamada **Veri kaynağı**'nı **data/raw/ (yerel dosyalar)** olarak
   değiştirin — yolak açılır menüleri `ALPN`, `Kenyon_Cell`, `MBON`, `DAN` gibi
   gerçek etiketlerle otomatik doldurulmalıdır. "Ulaşılan çıktı nöronu" KPI
   kartını kontrol edin — tam FAFB Mantar Cisimciği yolağı için varsayılan
   parametrelerle bu 96/96 olarak görünmelidir.
3. `python -m mbsim.cli --config configs/raw.yaml` — bir dakikanın altında
   tamamlanmalı ve özetinde aynı ulaşma sayısını yazdırmalı, ayrıca
   `outputs/` altına beş dosyanın tamamını yazmalıdır.
4. "Canlı Yayılım" sekmesini açın, **▶ Oynat**'a basın ve animasyonun
   ortasında hasarlı paneldeki ateşlenme sayısının sağlıklı panelin gerisinde
   kaldığını doğrulayın (gerçek veri setinde varsayılan parametrelerle, fark
   en büyük halini t≈0.04–0.08 civarında alır — örn. aynı anda kabaca 3300'e
   karşı 1500 nöron ateşlenmiş olur).

Bunlardan herhangi biri burada anlatılanla uyuşmuyorsa, yerel verinizde veya
yapılandırmanızda bu README'nin varsaydığından farklı bir şey var demektir —
önce beklenen tam sütunlar ve dosya adları için `data/raw/README.md`
dosyasına bakın.

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
  cli.py                          # toplu (batch) giriş noktası
configs/default.yaml       # CLI yapılandırması (örnek veri, PN/KC/MBON rolleri)
configs/raw.yaml           # gerçek veri için CLI yapılandırması (ALPN/Kenyon_Cell/MBON rolleri)
data/fixtures/             # sentetik demo verisi (git'te izlenir)
data/connectome/           # uygulamayla dağıtılan Princeton konektom alt kümesi (git'te izlenir)
data/raw/                  # kaynak Codex dışa aktarımları / yerel tam veri (gitignore'da)
data/lab/                  # Faz 2 sinek deneyi sonuçları, toplandığında buraya (gitignore'da)
data/clinical/             # Faz 3 insan görev sonuçları, toplandığında buraya (gitignore'da)
tests/                     # pytest test paketi
```
