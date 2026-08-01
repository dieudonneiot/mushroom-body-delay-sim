# Phase 3 clinical data (not tracked in git)

Nothing lands here yet — this project is still Phase 1 (in silico), and
Phase 3 requires Phase 2 lab validation first. This folder exists so the
clinical time-perception task results have a known home and a known shape
the moment they exist. `mbsim.validation` reads exactly this shape; with no
clinical data yet, that comparison cannot run for real, but the loader and
its self-test (synthetic data shaped like this file) are ready ahead of time.

## time_perception_task.csv

One row per patient per trial (the patient presses a button when they
believe a target interval — 5, 10, or 30s per the project plan — has
elapsed). See `time_perception_task.template.csv` for an empty file with
just the header row.

| column | type | meaning |
|---|---|---|
| patient_id | str | unique identifier for the patient |
| group | str | e.g. `"control"`, `"alzheimers"`, `"mci"` |
| target_interval_s | float | the interval the patient was asked to judge (5.0 / 10.0 / 30.0) |
| reported_time_s | float | elapsed time when the patient pressed the button, from trial start |
| simple_reaction_time_s | float | the patient's own motor baseline (measured once per session — how fast they can physically press a button), used to subtract out button-press lag so what's measured is time perception, not motor reflex |
| heart_rate_bpm | float, optional | pulse-sensor reading during the trial — a stress/excitement covariate, so a delay caused by anxiety can be statistically separated from one caused by genuine neurological slowing, per the project pitch |

`mbsim.validation.load_time_perception_task` computes each patient's
corrected perceived time (`reported_time_s - simple_reaction_time_s`) and
its % deviation from `target_interval_s` — a human-scale analog of the
simulation's %-deviation output — then aggregates by group the same way the
fly climbing assay is aggregated (see `mbsim.validation.compare_to_simulation`).
