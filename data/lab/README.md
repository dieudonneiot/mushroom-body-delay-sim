# Phase 2 lab data (not tracked in git)

Nothing lands here yet — this project is still Phase 1 (in silico). This
folder exists so the wet-lab negative-geotaxis (climbing) assay results have
a known home and a known shape the moment they exist, instead of that being
figured out ad hoc later. `mbsim.validation` (see `src/mbsim/validation.py`)
reads exactly this shape to compute the sim-vs-lab comparison described in
the project pitch — no lab data currently exists, so that comparison cannot
run for real yet; `mbsim.validation`'s self-test uses synthetic data shaped
like this file to prove the comparison logic itself is correct ahead of time.

## climbing_assay.csv

One row per fly per trial (negative geotaxis: time to climb a fixed
distance after being tapped to the bottom of the vial). See
`climbing_assay.template.csv` for an empty file with just the header row.

| column | type | meaning |
|---|---|---|
| group | str | `"control"` or `"alzheimers_model"` |
| fly_id | str | unique identifier for the individual fly |
| trial | int | trial number, for flies measured more than once |
| climb_time_s | float | seconds to climb the fixed distance |

Per this project's Phase 2 plan: ~150 Alzheimer's-model flies + ~150 healthy
controls (see the main [README.md](../../README.md) project overview).

`mbsim.validation.load_climbing_assay` reads this and computes each group's
mean climb time and the % deviation of `alzheimers_model` vs. `control` —
the same %-deviation quantity `mbsim.metrics.compare` reports for the
simulated network, so the two numbers land in directly comparable units
(see `mbsim.validation.compare_to_simulation`).

## visual_perception_assay.csv (optional, same shape)

The project pitch also mentions a visual perception behavioral test in
Phase 2. If/when that's run, save it in the same shape as
`climbing_assay.csv` but with a `response_time_s` column instead of
`climb_time_s` (whatever the task's measured latency is) — `mbsim.validation`
treats "group + a single per-trial latency column" generically, so no new
loader is needed, just point `load_climbing_assay` at the file (the function
name is a placeholder; rename if a second, genuinely different assay shape
shows up).
