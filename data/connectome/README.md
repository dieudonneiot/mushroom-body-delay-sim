# Bundled Princeton connectome subset

These two CSVs are the app-ready subset generated from the Codex exports
`connections_princeton.csv.gz` and `classification.csv.gz` downloaded on
2026-10-11. The export did not include an identifiable dataset release in the
filenames, so record the Codex release/version here when it is confirmed.

The subset contains only neurons classified as `ALPN`, `Kenyon_Cell`, or
`MBON`, and only connections whose pre- and post-neurons are both in those
groups. The prepared files contain 5,958 neurons and 143,943 connections.
Connection neurotransmitter and neuropil fields are retained for the app's
perturbation controls.

To regenerate after downloading a new pair of exports, put the compressed
source files in `data/raw/` and run from the repository root:

```powershell
python scripts/prepare_connectome.py data/raw/connections_princeton.csv.gz data/raw/classification.csv.gz
```

The app loads this compact subset by default. The original compressed exports
are local inputs and remain excluded from Git; the prepared subset is tracked
so it is present in the Streamlit Community Cloud deployment.
