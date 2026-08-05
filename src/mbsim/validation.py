"""Compare simulated %-deviation output against Phase 2/3 empirical data.

Nothing here can run against real data yet — no lab (`data/lab/`) or
clinical (`data/clinical/`) data exists (see those folders' `README.md` for
the expected CSV shape, since neither has been collected). This module's
loaders and `compare_to_simulation` are still fully exercised now, against
synthetic data shaped like the real files (see `tests/test_validation.py`),
so the comparison logic is written and verified ahead of time rather than
from scratch under Phase 2/3 time pressure.

The project's stated validation goal is not an exact percentage match across
the fly simulation, the fly lab assay, and the human clinical task — it's a
same-direction, meaningful-magnitude deviation across all three (e.g. a 30%
simulated deviation and a 28-32% measured one both count as validating;
30% vs. -5%, or 30% vs. 2%, would not). `compare_to_simulation` reports the
raw % deviations side by side plus a same-direction boolean, deliberately
not a single pass/fail score — "close enough" is the medical team's
judgment call, not this module's.
"""

import pandas as pd

CLIMBING_ASSAY_REQUIRED_COLUMNS = {"group", "fly_id", "trial", "climb_time_s"}
TIME_PERCEPTION_REQUIRED_COLUMNS = {
    "patient_id",
    "group",
    "target_interval_s",
    "reported_time_s",
    "simple_reaction_time_s",
}


def load_climbing_assay(path) -> pd.DataFrame:
    """Load a Phase 2 negative-geotaxis (or shape-compatible visual-perception)
    assay export — see `data/lab/README.md` for the expected columns."""
    df = pd.read_csv(path)
    missing = CLIMBING_ASSAY_REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"{path} is missing required column(s) {sorted(missing)}")
    return df


def climbing_assay_pct_deviation(
    df: pd.DataFrame, damaged_group: str = "alzheimers_model", healthy_group: str = "control"
) -> float:
    """% deviation of the damaged group's mean climb time from the healthy
    group's — the same quantity, and the same formula, as
    `mbsim.metrics.compare`'s `pct_deviation` for the simulated network."""
    healthy_mean = df.loc[df["group"] == healthy_group, "climb_time_s"].mean()
    damaged_mean = df.loc[df["group"] == damaged_group, "climb_time_s"].mean()
    if pd.isna(healthy_mean) or pd.isna(damaged_mean):
        raise ValueError(f"Need at least one '{healthy_group}' row and one '{damaged_group}' row")
    if healthy_mean == 0:
        raise ValueError(f"'{healthy_group}' mean climb_time_s is zero — cannot compute a % deviation")
    return (damaged_mean - healthy_mean) / healthy_mean * 100


def _add_time_perception_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["corrected_perceived_time_s"] = df["reported_time_s"] - df["simple_reaction_time_s"]
    df["pct_deviation"] = (
        (df["corrected_perceived_time_s"] - df["target_interval_s"]) / df["target_interval_s"] * 100
    )
    return df


def load_time_perception_task(path) -> pd.DataFrame:
    """Load a Phase 3 clinical time-perception task export — see
    `data/clinical/README.md` for the expected columns. Adds
    `corrected_perceived_time_s` (button-press lag subtracted out) and
    `pct_deviation` (that corrected time vs. the target interval) columns."""
    df = pd.read_csv(path)
    missing = TIME_PERCEPTION_REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"{path} is missing required column(s) {sorted(missing)}")
    return _add_time_perception_derived_columns(df)


def example_climbing_assay() -> pd.DataFrame:
    """Synthetic Phase 2 climbing-assay data, shaped like
    `data/lab/climbing_assay.template.csv`, for demoing the validation
    comparison before real lab data exists. Not real data —
    `alzheimers_model` flies climb 30% slower than `control` by construction."""
    return pd.DataFrame(
        {
            "group": ["control"] * 3 + ["alzheimers_model"] * 3,
            "fly_id": ["c1", "c2", "c3", "a1", "a2", "a3"],
            "trial": [1, 1, 1, 1, 1, 1],
            "climb_time_s": [10.0, 10.0, 10.0, 13.0, 13.0, 13.0],
        }
    )


def example_time_perception_task() -> pd.DataFrame:
    """Synthetic Phase 3 clinical time-perception data, shaped like
    `data/clinical/time_perception_task.template.csv` (already run through
    `load_time_perception_task`'s derived-column logic), for demoing the
    validation comparison before real patient data exists. Not real data —
    `control` patients perceive the target interval accurately (0% deviation
    after reaction-time correction); `alzheimers` patients perceive time as
    passing more slowly (+30% deviation), matching the project pitch's worked
    example (10s target, pressed at 13s)."""
    raw = pd.DataFrame(
        {
            "patient_id": ["p1", "p2", "p3", "p4"],
            "group": ["control", "control", "alzheimers", "alzheimers"],
            "target_interval_s": [10.0, 10.0, 10.0, 10.0],
            "reported_time_s": [10.2, 10.2, 13.2, 13.2],
            "simple_reaction_time_s": [0.2, 0.2, 0.2, 0.2],
        }
    )
    return _add_time_perception_derived_columns(raw)


def time_perception_group_deviation(df: pd.DataFrame, group: str) -> float:
    """Mean %-deviation-from-target-interval for one group (e.g. "control" or
    "alzheimers")."""
    subset = df.loc[df["group"] == group, "pct_deviation"]
    if subset.empty:
        raise ValueError(f"No rows for group {group!r}")
    return subset.mean()


def time_perception_excess_deviation(
    df: pd.DataFrame, damaged_group: str = "alzheimers", healthy_group: str = "control"
) -> float:
    """The damaged group's mean %-deviation-from-target minus the healthy
    group's — nets out any baseline perception bias common to everyone,
    isolating the disease-specific component. This is the human-scale
    quantity most directly comparable to the fly/simulation %deviation
    (which have no separate ground-truth "target" to net out against, only
    a damaged-vs-healthy comparison)."""
    return time_perception_group_deviation(df, damaged_group) - time_perception_group_deviation(df, healthy_group)


def compare_to_simulation(
    sim_pct_deviation: float,
    climbing_df: pd.DataFrame | None = None,
    clinical_df: pd.DataFrame | None = None,
    climbing_damaged_group: str = "alzheimers_model",
    climbing_healthy_group: str = "control",
    clinical_damaged_group: str = "alzheimers",
    clinical_healthy_group: str = "control",
) -> dict:
    """Side-by-side comparison of the simulated %-deviation against whichever
    of the Phase 2 (fly) / Phase 3 (human) empirical %-deviations are
    available. Reports raw numbers plus a same-direction boolean per source —
    not a single score, see module docstring."""
    result: dict = {"simulation_pct_deviation": sim_pct_deviation}

    if climbing_df is not None:
        fly_pct_deviation = climbing_assay_pct_deviation(
            climbing_df, climbing_damaged_group, climbing_healthy_group
        )
        result["fly_pct_deviation"] = fly_pct_deviation
        result["fly_same_direction_as_simulation"] = bool((fly_pct_deviation > 0) == (sim_pct_deviation > 0))

    if clinical_df is not None:
        human_excess_pct_deviation = time_perception_excess_deviation(
            clinical_df, clinical_damaged_group, clinical_healthy_group
        )
        result["human_excess_pct_deviation"] = human_excess_pct_deviation
        result["human_same_direction_as_simulation"] = bool(
            (human_excess_pct_deviation > 0) == (sim_pct_deviation > 0)
        )

    return result
