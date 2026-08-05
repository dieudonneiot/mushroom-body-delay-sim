import pandas as pd
import pytest

from mbsim.validation import (
    climbing_assay_pct_deviation,
    compare_to_simulation,
    example_climbing_assay,
    example_time_perception_task,
    load_climbing_assay,
    load_time_perception_task,
    time_perception_excess_deviation,
    time_perception_group_deviation,
)


def _climbing_df():
    # Synthetic, shaped like data/lab/climbing_assay.template.csv — alzheimers_model
    # flies climb ~30% slower than controls.
    return pd.DataFrame(
        {
            "group": ["control"] * 3 + ["alzheimers_model"] * 3,
            "fly_id": ["c1", "c2", "c3", "a1", "a2", "a3"],
            "trial": [1, 1, 1, 1, 1, 1],
            "climb_time_s": [10.0, 10.0, 10.0, 13.0, 13.0, 13.0],
        }
    )


def _clinical_df():
    # Synthetic, shaped like data/clinical/time_perception_task.template.csv.
    # Controls perceive target intervals accurately (0% deviation after
    # reaction-time correction); alzheimers patients perceive time as passing
    # more slowly, pressing later than the target (+30% deviation), matching
    # the project pitch's worked example (10s target, pressed at 13s).
    return pd.DataFrame(
        {
            "patient_id": ["p1", "p2", "p3", "p4"],
            "group": ["control", "control", "alzheimers", "alzheimers"],
            "target_interval_s": [10.0, 10.0, 10.0, 10.0],
            "reported_time_s": [10.2, 10.2, 13.2, 13.2],
            "simple_reaction_time_s": [0.2, 0.2, 0.2, 0.2],
        }
    )


def test_load_climbing_assay_requires_expected_columns(tmp_path):
    path = tmp_path / "climbing_assay.csv"
    _climbing_df().to_csv(path, index=False)
    df = load_climbing_assay(path)
    assert len(df) == 6


def test_load_climbing_assay_raises_on_missing_column(tmp_path):
    path = tmp_path / "bad.csv"
    _climbing_df().drop(columns=["climb_time_s"]).to_csv(path, index=False)
    with pytest.raises(ValueError, match="climb_time_s"):
        load_climbing_assay(path)


def test_climbing_assay_pct_deviation_matches_hand_calculation():
    deviation = climbing_assay_pct_deviation(_climbing_df())
    assert abs(deviation - 30.0) < 1e-9


def test_climbing_assay_pct_deviation_raises_without_both_groups():
    df = _climbing_df()
    df = df[df["group"] == "control"]
    with pytest.raises(ValueError):
        climbing_assay_pct_deviation(df)


def test_time_perception_task_adds_corrected_and_deviation_columns():
    df = load_time_perception_task_from_frame(_clinical_df())
    assert abs(df.loc[0, "corrected_perceived_time_s"] - 10.0) < 1e-9
    assert abs(df.loc[0, "pct_deviation"] - 0.0) < 1e-9
    assert abs(df.loc[2, "pct_deviation"] - 30.0) < 1e-9


def load_time_perception_task_from_frame(df):
    # load_time_perception_task takes a path; reuse its column logic via a
    # round-trip through a temp-free in-memory CSV buffer for this unit test.
    import io

    buf = io.StringIO()
    df.to_csv(buf, index=False)
    buf.seek(0)
    return load_time_perception_task(buf)


def test_time_perception_group_deviation_isolates_disease_effect():
    df = load_time_perception_task_from_frame(_clinical_df())
    control_dev = time_perception_group_deviation(df, "control")
    alz_dev = time_perception_group_deviation(df, "alzheimers")
    assert abs(control_dev - 0.0) < 1e-9
    assert abs(alz_dev - 30.0) < 1e-9


def test_time_perception_excess_deviation_nets_out_baseline_bias():
    df = load_time_perception_task_from_frame(_clinical_df())
    excess = time_perception_excess_deviation(df)
    assert abs(excess - 30.0) < 1e-9


def test_compare_to_simulation_reports_same_direction_for_matching_signs():
    climbing_df = _climbing_df()
    clinical_df = load_time_perception_task_from_frame(_clinical_df())
    result = compare_to_simulation(28.0, climbing_df=climbing_df, clinical_df=clinical_df)
    assert result["simulation_pct_deviation"] == 28.0
    assert abs(result["fly_pct_deviation"] - 30.0) < 1e-9
    assert result["fly_same_direction_as_simulation"] is True
    assert abs(result["human_excess_pct_deviation"] - 30.0) < 1e-9
    assert result["human_same_direction_as_simulation"] is True


def test_compare_to_simulation_flags_opposite_direction():
    climbing_df = _climbing_df()
    result = compare_to_simulation(-10.0, climbing_df=climbing_df)
    assert result["fly_same_direction_as_simulation"] is False


def test_compare_to_simulation_omits_sources_not_provided():
    result = compare_to_simulation(28.0)
    assert "fly_pct_deviation" not in result
    assert "human_excess_pct_deviation" not in result


def test_example_climbing_assay_is_loadable_and_matches_documented_deviation():
    df = example_climbing_assay()
    assert {"group", "fly_id", "trial", "climb_time_s"} <= set(df.columns)
    assert abs(climbing_assay_pct_deviation(df) - 30.0) < 1e-9


def test_example_time_perception_task_matches_documented_deviation():
    df = example_time_perception_task()
    assert abs(time_perception_excess_deviation(df) - 30.0) < 1e-9
