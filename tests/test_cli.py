from pathlib import Path

import pytest
import yaml

from mbsim.cli import run


def test_unknown_data_mode_raises_instead_of_silently_using_fixture_data(tmp_path):
    """Any data.mode other than the exact strings 'raw'/'fixture' (a typo, or
    the Streamlit app's 'upload' mode, which the CLI doesn't implement) must
    raise, not silently fall back to the small fixture graph."""
    config = {
        "data": {"mode": "upload", "raw_dir": "data/raw", "fixture_dir": "data/fixtures"},
        "roles": {"input": ["PN"], "relay": ["KC"], "output": ["MBON"]},
        "simulation": {"conduction_velocity": 1.0, "threshold": 1.0},
        "damage": {"perturbations": []},
        "output": {"dir": str(tmp_path / "out")},
    }
    config_path = tmp_path / "config.yaml"
    config_path.write_text(yaml.safe_dump(config))

    with pytest.raises(ValueError, match="Unknown data.mode"):
        run(str(config_path))
