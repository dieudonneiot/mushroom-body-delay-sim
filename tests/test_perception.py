import numpy as np
import pytest

from mbsim.perception import time_perception_deviation, weber_fechner_curve


def test_weber_fechner_curve_is_monotonically_increasing():
    t = np.linspace(0.1, 30.0, 50)
    curve = weber_fechner_curve(t, k=1.0)
    assert np.all(np.diff(curve) > 0)


def test_equal_delays_give_zero_deviation():
    result = time_perception_deviation(5.0, 5.0)
    assert result["pct_deviation"] == 0.0
    assert np.allclose(result["healthy"], result["damaged"])


def test_larger_damaged_delay_gives_positive_deviation_and_lower_curve():
    result = time_perception_deviation(5.0, 6.5)
    assert result["pct_deviation"] > 0
    assert np.all(result["damaged"] <= result["healthy"] + 1e-12)


def test_pct_deviation_matches_metrics_compares_formula_exactly():
    """Regression test for the bug where this module's pct_deviation (then a
    vertical k-rescale curve-gap) numerically disagreed with
    mbsim.metrics.compare's pct_deviation ((damaged-healthy)/healthy*100) for
    the same healthy/damaged pair — e.g. 23.1% here vs. 30% there for 5.0ms
    -> 6.5ms. Both must report the identical figure for the same comparison."""
    healthy_ms, damaged_ms = 200.0, 260.0
    result = time_perception_deviation(healthy_ms, damaged_ms)
    expected = (damaged_ms - healthy_ms) / healthy_ms * 100
    assert result["pct_deviation"] == pytest.approx(expected)
    assert result["pct_deviation"] == pytest.approx(30.0)


def test_nonpositive_delay_falls_back_to_zero_curve():
    result = time_perception_deviation(0.0, 6.5)
    assert result["pct_deviation"] == 0.0
    assert np.all(result["healthy"] == 0.0)
    assert np.all(result["damaged"] == 0.0)
