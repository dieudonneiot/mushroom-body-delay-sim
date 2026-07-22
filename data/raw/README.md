# Raw data (not tracked in git)

**English:**

Put the manually-exported FlyWire/Codex CSVs here:

1. Log in at https://codex.flywire.ai (free account).
2. Go to **Info -> Download Data**, pick the latest dataset version (e.g. `fafb` / female adult fly brain).
3. Export and place here as:
   - `connections.csv` — columns: `pre_root_id, post_root_id, neuropil, syn_count, nt_type` (exact column names may vary slightly by release; `mbsim.io` will tell you if a required column is missing).
   - `classification.csv` — columns: `root_id, cell_type` (or similar), containing class labels such as Kenyon cell ("KC"), mushroom body output neuron ("MBON"), projection neuron ("PN"), mushroom body input neuron / dopaminergic neuron ("MBIN"/"DAN").

Until these are in place, the pipeline (both `streamlit run app.py` and
`python -m mbsim.cli`) can be developed and tested against the small synthetic
graph in `data/fixtures/`. In the interactive UI you can also skip this folder
entirely and use the "Upload CSVs" data source instead.

---

**Türkçe:**

Elle dışa aktarılan FlyWire/Codex CSV dosyalarını buraya koyun:

1. https://codex.flywire.ai adresinden giriş yapın (ücretsiz hesap).
2. **Info -> Download Data** bölümüne gidin, en güncel veri seti sürümünü seçin (örn. `fafb` / dişi yetişkin sinek beyni).
3. Dışa aktarıp buraya şu şekilde yerleştirin:
   - `connections.csv` — sütunlar: `pre_root_id, post_root_id, neuropil, syn_count, nt_type` (sürüme göre tam sütun adları hafifçe değişebilir; gerekli bir sütun eksikse `mbsim.io` bunu size bildirir).
   - `classification.csv` — sütunlar: `root_id, cell_type` (veya benzeri), Kenyon hücresi ("KC"), mantar cisimciği çıktı nöronu ("MBON"), projeksiyon nöronu ("PN"), mantar cisimciği girdi nöronu / dopaminerjik nöron ("MBIN"/"DAN") gibi sınıf etiketlerini içerir.

Bunlar hazır olana kadar, işlem hattı (`streamlit run app.py` ve
`python -m mbsim.cli` ikisi de) `data/fixtures/` içindeki küçük sentetik grafik
üzerinde geliştirilip test edilebilir. Etkileşimli arayüzde bu klasörü
tamamen atlayıp bunun yerine "CSV yükle" veri kaynağını da kullanabilirsiniz.
