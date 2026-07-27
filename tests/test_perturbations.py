from mbsim.perturbations import combined_severity


def test_empty_list_gives_zero_severity():
    assert combined_severity([]) == 0.0


def test_single_perturbation_matches_its_reduction_fn():
    severity = combined_severity([{"type": "tau", "intensity": 18.0}])
    assert abs(severity - 0.18) < 1e-9


def test_two_perturbations_combine_multiplicatively():
    severity = combined_severity(
        [
            {"type": "tau", "intensity": 18.0},
            {"type": "amyloid", "intensity": 10.0},
        ]
    )
    expected = 1.0 - (1.0 - 0.18) * (1.0 - 0.10)
    assert abs(severity - expected) < 1e-9
    assert severity < 1.0
    # Not simple addition (0.28) and not an overwrite (0.18/0.10).
    assert abs(severity - 0.28) > 1e-9


def test_zero_intensity_and_unknown_type_are_ignored():
    severity = combined_severity(
        [
            {"type": "tau", "intensity": 0.0},
            {"type": "not_a_real_type", "intensity": 50.0},
        ]
    )
    assert severity == 0.0


def test_many_perturbations_stay_below_one():
    perturbations = [{"type": "tau", "intensity": 90.0} for _ in range(5)]
    assert combined_severity(perturbations) < 1.0
