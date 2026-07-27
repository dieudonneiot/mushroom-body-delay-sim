import numpy as np

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


def test_nonpositive_delay_falls_back_to_zero_curve():
    result = time_perception_deviation(0.0, 6.5)
    assert result["pct_deviation"] == 0.0
    assert np.all(result["healthy"] == 0.0)
    assert np.all(result["damaged"] == 0.0)
