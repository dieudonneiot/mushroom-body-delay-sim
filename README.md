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
python -m venv .venv
.venv/Scripts/activate   # .venv/bin/activate on macOS/Linux
pip install -e ".[dev]"
```

This installs the `mbsim` package plus `streamlit`, `plotly`, `networkx`, `pandas`,
`matplotlib`, `pyyaml`, and (via `[dev]`) `pytest`.

### 2. Getting the real connectome data

Codex does not offer a general bulk API — data is exported manually as CSV. See
[data/raw/README.md](data/raw/README.md) for the exact steps and expected columns.
Until that's done, everything runs against the small synthetic graph in
`data/fixtures/` (3 PN, 6 KC, 2 MBON neurons, fully wired) so you can try every
feature immediately with no setup.

### 3. Interactive UI (recommended)

```
streamlit run app.py
```

This opens a browser tab. Every detail of what's on screen:

**Language toggle** — at the very top of the sidebar, a switch between
**English** and **Türkçe**. It re-translates every label, button, tab, warning,
chart title, and even the graph hover tooltips — nothing is left in the other
language. Switch it anytime; your other settings (sliders, data source) are kept.

**Sidebar — Data source**
- *Fixture (demo data)* — the small synthetic graph in `data/fixtures/`, always available, no setup needed.
- *data/raw/ (local files)* — reads `connections.csv` + `classification.csv` you've placed in `data/raw/` per the instructions in `data/raw/README.md`. If the files aren't there, you'll get a clear on-screen error telling you what's missing and where to look.
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

**Main area — "Comparison" tab**
A grouped bar chart: healthy vs. damaged arrival time, one pair of bars per
output neuron. This is the chart form of the same numbers as the CSV in the
"Data" tab.

**Main area — "Data" tab**
The raw comparison table (one row per output neuron reached: healthy time,
damaged time, % deviation) plus a "Download comparison.csv" button to save it
locally for further analysis or sharing with the medical team.

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

Edit `configs/default.yaml` to change, without touching code:
- `data.mode`: `fixture` or `raw` (switch to `raw` once real data is in `data/raw/`)
- `roles`: which cell types count as input/relay/output
- `simulation.conduction_velocity`, `simulation.threshold`
- `damage.severity`
- `output.dir`: where results are written

### 5. Extending with a real damage model

`src/mbsim/damage.py` has one placeholder slowdown function (`linear_slowdown`:
velocity reduction scales linearly with severity in [0, 1]). Once the medical
team provides a literature-derived function (severity -> conduction velocity
reduction), write it there and pass it as `slowdown_fn` to
`mbsim.metrics.compare(...)` (already wired into both `app.py` and `cli.py`) —
no changes needed anywhere else in the pipeline.

### 6. Tests

```
pytest
```

All tests run against the synthetic fixture in `data/fixtures/`, so they don't
require the real Codex download.

### Project structure

```
app.py                    # Streamlit interactive UI
src/mbsim/
  io.py                   # load + validate Codex CSV exports
  mushroom_body.py        # filter to the configured input/relay/output pathway
  graph.py                # NetworkX graph construction + sanity checks
  simulation.py           # event-driven signal propagation
  damage.py               # severity -> conduction velocity slowdown (pluggable)
  metrics.py              # healthy vs. damaged comparison + % deviation
  layout.py               # shared node layout / role colors
  visualize.py            # static matplotlib figures (used by the CLI)
  plotly_viz.py           # interactive Plotly figures (used by the app)
  i18n.py                 # English/Turkish UI string translations
  cli.py                  # batch entrypoint
configs/default.yaml      # CLI configuration
data/fixtures/            # synthetic demo data (tracked in git)
data/raw/                 # real Codex export goes here (gitignored)
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
python -m venv .venv
.venv/Scripts/activate   # macOS/Linux'ta .venv/bin/activate
pip install -e ".[dev]"
```

Bu komut `mbsim` paketini ve `streamlit`, `plotly`, `networkx`, `pandas`,
`matplotlib`, `pyyaml` ile (`[dev]` sayesinde) `pytest`'i kurar.

### 2. Gerçek konektom verisini edinme

Codex genel/toplu bir API sunmuyor — veri, elle CSV olarak dışa aktarılır.
Kesin adımlar ve beklenen sütunlar için [data/raw/README.md](data/raw/README.md)
dosyasına bakın. Bu işlem yapılana kadar her şey `data/fixtures/` içindeki küçük
sentetik grafik (3 PN, 6 KC, 2 MBON nöronu, tamamen bağlı) üzerinde çalışır;
böylece hiçbir kurulum yapmadan tüm özellikleri hemen deneyebilirsiniz.

### 3. Etkileşimli Arayüz (önerilen)

```
streamlit run app.py
```

Bu komut tarayıcıda bir sekme açar. Ekrandaki her şeyin ayrıntısı:

**Dil seçici (Language toggle)** — kenar çubuğunun en üstünde, **English** ve
**Türkçe** arasında bir geçiş anahtarı. Her etiketi, düğmeyi, sekmeyi, uyarıyı,
grafik başlığını ve hatta grafik üzerindeki ipucu (hover tooltip) metinlerini
yeniden çevirir — hiçbir şey diğer dilde kalmaz. İstediğiniz zaman
değiştirebilirsiniz; diğer ayarlarınız (kaydırıcılar, veri kaynağı) korunur.

**Kenar çubuğu — Veri kaynağı**
- *Örnek veri (demo)* — `data/fixtures/` içindeki küçük sentetik grafik; her zaman kullanılabilir, kurulum gerekmez.
- *data/raw/ (yerel dosyalar)* — `data/raw/README.md` dosyasındaki talimatlara göre `data/raw/` klasörüne koyduğunuz `connections.csv` + `classification.csv` dosyalarını okur. Dosyalar orada değilse, neyin eksik olduğunu ve nereye bakmanız gerektiğini açıkça belirten bir hata mesajı görürsünüz.
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

**Ana alan — "Karşılaştırma" sekmesi**
Gruplandırılmış bir çubuk grafik: her çıktı nöronu için sağlıklı ve hasarlı
varış zamanı bir çift çubuk olarak gösterilir. Bu, "Veri" sekmesindeki CSV ile
aynı sayıların grafik biçimidir.

**Ana alan — "Veri" sekmesi**
Ham karşılaştırma tablosu (ulaşılan her çıktı nöronu için bir satır: sağlıklı
zaman, hasarlı zaman, % sapma) ve bunu yerel olarak kaydetmek veya tıp ekibiyle
paylaşmak için bir "comparison.csv dosyasını indir" düğmesi.

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

Koda dokunmadan değiştirmek için `configs/default.yaml` dosyasını düzenleyin:
- `data.mode`: `fixture` veya `raw` (gerçek veri `data/raw/` içine konduğunda `raw`'a geçin)
- `roles`: hangi hücre tiplerinin girdi/aktarıcı/çıktı sayılacağı
- `simulation.conduction_velocity`, `simulation.threshold`
- `damage.severity`
- `output.dir`: sonuçların yazılacağı yer

### 5. Gerçek bir hasar modeliyle genişletme

`src/mbsim/damage.py` içinde tek bir yer tutucu yavaşlatma fonksiyonu bulunur
(`linear_slowdown`: hız azalması [0, 1] aralığında şiddetle doğrusal olarak
ölçeklenir). Tıp ekibi literatüre dayalı bir fonksiyon sağladığında (şiddet ->
iletim hızı azalması), bunu oraya yazın ve `mbsim.metrics.compare(...)`
fonksiyonuna `slowdown_fn` olarak geçirin (hem `app.py` hem de `cli.py`'de zaten
bağlanmıştır) — işlem hattının başka hiçbir yerinde değişiklik gerekmez.

### 6. Testler

```
pytest
```

Tüm testler `data/fixtures/` içindeki sentetik veriye karşı çalışır; bu yüzden
gerçek Codex indirmesine ihtiyaç duymazlar.

### Proje yapısı

```
app.py                    # Streamlit etkileşimli arayüz
src/mbsim/
  io.py                   # Codex CSV dışa aktarımlarını yükler + doğrular
  mushroom_body.py         # yapılandırılan girdi/aktarıcı/çıktı yolağına göre filtreler
  graph.py                 # NetworkX grafik oluşturma + sağlık kontrolleri
  simulation.py            # olay-tabanlı sinyal yayılımı
  damage.py                 # şiddet -> iletim hızı yavaşlaması (değiştirilebilir)
  metrics.py                # sağlıklı/hasarlı karşılaştırma + % sapma
  layout.py                  # ortak nöron yerleşimi / rol renkleri
  visualize.py                # statik matplotlib grafikleri (CLI tarafından kullanılır)
  plotly_viz.py                 # etkileşimli Plotly grafikleri (uygulama tarafından kullanılır)
  i18n.py                        # İngilizce/Türkçe arayüz metni çevirileri
  cli.py                          # toplu (batch) giriş noktası
configs/default.yaml       # CLI yapılandırması
data/fixtures/             # sentetik demo verisi (git'te izlenir)
data/raw/                  # gerçek Codex dışa aktarımı buraya konur (gitignore'da)
tests/                     # pytest test paketi
```
