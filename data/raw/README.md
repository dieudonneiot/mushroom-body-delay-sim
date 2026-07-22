# Raw data (not tracked in git)

**English:**

Put the manually-exported FlyWire/Codex CSVs here:

1. Log in at https://codex.flywire.ai (free account).
2. Go to the download icon in the top bar (**Downloadable assets**), pick the
   latest dataset version (e.g. `FAFB` / female adult fly brain).
3. Download exactly these two files and place them here **renamed** as shown
   (verified against the real FAFB v783 export):
   - **"Connections (Filtered)"** → save as `connections.csv`. Columns:
     `pre_root_id, post_root_id, neuropil, syn_count, nt_type`. Prefer the
     *Filtered* variant over *Unfiltered* — it's much smaller (tens of MB vs.
     hundreds of MB) and strips low-confidence noise; both have an identical
     schema, so either works.
   - **"Classification / Hierarchical Annotations"** → save as
     `classification.csv`. Columns: `root_id, flow, super_class, class,
     sub_class, hemilineage, side, nerve` — **there is no `cell_type` column**
     in current Codex exports. `mbsim.io.load_classification` automatically
     aliases `class` → `cell_type`, since that's the column carrying the
     values this pipeline needs: `Kenyon_Cell` (relay), `MBON` (output),
     `ALPN` (the antennal-lobe projection neurons — the real-data equivalent
     of the fixture's `PN`, use as input), plus `DAN`/`MBIN` if you want to
     add the modulatory dopaminergic pathway as an extra role.

   Do **not** download "Synapse Table" (multiple GB, per-synapse rows) or
   "Neuron Skeletons" (also GB-scale, 3D morphology) — this pipeline is a pure
   graph/topology model and never reads either.

4. Either edit `configs/default.yaml` (`data.mode: raw`, and update `roles` to
   `ALPN`/`Kenyon_Cell`/`MBON`), or just use the ready-made
   [configs/raw.yaml](../configs/raw.yaml), which already has both set:
   `python -m mbsim.cli --config configs/raw.yaml`.

Until these are in place, the pipeline (both `streamlit run app.py` and
`python -m mbsim.cli`) can be developed and tested against the small synthetic
graph in `data/fixtures/` (labeled `PN`/`KC`/`MBON`). In the interactive UI you
can also skip this folder entirely and use the "Upload CSVs" data source
instead.

---

**Türkçe:**

Elle dışa aktarılan FlyWire/Codex CSV dosyalarını buraya koyun:

1. https://codex.flywire.ai adresinden giriş yapın (ücretsiz hesap).
2. Üst çubuktaki indirme simgesine (**Downloadable assets**) gidin, en güncel
   veri seti sürümünü seçin (örn. `FAFB` / dişi yetişkin sinek beyni).
3. Tam olarak şu iki dosyayı indirip aşağıdaki gibi **yeniden adlandırarak**
   buraya yerleştirin (gerçek FAFB v783 dışa aktarımına karşı doğrulanmıştır):
   - **"Connections (Filtered)"** → `connections.csv` olarak kaydedin. Sütunlar:
     `pre_root_id, post_root_id, neuropil, syn_count, nt_type`. *Unfiltered*
     yerine *Filtered* sürümünü tercih edin — çok daha küçüktür (yüzlerce MB
     yerine onlarca MB) ve düşük güvenilirlikli gürültüyü ayıklar; ikisinin de
     şeması aynıdır, bu yüzden hangisini seçerseniz seçin çalışır.
   - **"Classification / Hierarchical Annotations"** → `classification.csv`
     olarak kaydedin. Sütunlar: `root_id, flow, super_class, class, sub_class,
     hemilineage, side, nerve` — güncel Codex dışa aktarımlarında **`cell_type`
     sütunu yoktur**. `mbsim.io.load_classification` bu durumda otomatik
     olarak `class` sütununu `cell_type` olarak eşler, çünkü bu işlem hattının
     ihtiyaç duyduğu değerleri taşıyan sütun odur: `Kenyon_Cell` (aktarıcı),
     `MBON` (çıktı), `ALPN` (anten lobu projeksiyon nöronları — örnek verideki
     `PN`'nin gerçek veri karşılığı, girdi olarak kullanın), isterseniz
     düzenleyici dopaminerjik yolağı ekstra bir rol olarak eklemek için de
     `DAN`/`MBIN`.

   "Synapse Table" (birkaç GB, sinaps başına satır) veya "Neuron Skeletons"
   (yine GB ölçeğinde, 3B morfoloji) dosyalarını **indirmeyin** — bu işlem
   hattı saf bir graf/topoloji modelidir ve ikisini de hiçbir zaman okumaz.

4. `configs/default.yaml` dosyasını düzenleyin (`data.mode: raw` yapın ve
   `roles`'u `ALPN`/`Kenyon_Cell`/`MBON` olarak güncelleyin) ya da doğrudan
   hazır [configs/raw.yaml](../configs/raw.yaml) dosyasını kullanın — ikisi de
   zaten ayarlanmış durumda: `python -m mbsim.cli --config configs/raw.yaml`.

Bunlar hazır olana kadar, işlem hattı (`streamlit run app.py` ve
`python -m mbsim.cli` ikisi de) `data/fixtures/` içindeki küçük sentetik grafik
(`PN`/`KC`/`MBON` etiketli) üzerinde geliştirilip test edilebilir. Etkileşimli
arayüzde bu klasörü tamamen atlayıp bunun yerine "CSV yükle" veri kaynağını da
kullanabilirsiniz.
