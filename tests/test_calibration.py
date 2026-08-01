from mbsim.calibration import ms_per_time_unit


def test_ms_per_time_unit_is_positive():
    assert ms_per_time_unit() > 0
