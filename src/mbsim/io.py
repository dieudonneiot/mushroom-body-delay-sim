"""Load and validate FlyWire/Codex CSV exports (or the local dev fixtures)."""

from pathlib import Path

import pandas as pd

CONNECTIONS_REQUIRED_COLUMNS = ["pre_root_id", "post_root_id", "syn_count"]
CLASSIFICATION_REQUIRED_COLUMNS = ["root_id", "cell_type"]


def _validate_columns(df: pd.DataFrame, required: list[str], source: str) -> None:
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(
            f"{source} is missing required column(s) {missing}. "
            f"Found columns: {list(df.columns)}. "
            "Codex export schemas can vary slightly by release — "
            "update CONNECTIONS_REQUIRED_COLUMNS/CLASSIFICATION_REQUIRED_COLUMNS "
            "in mbsim/io.py or rename the CSV columns to match."
        )


def load_connections(path: Path | str) -> pd.DataFrame:
    df = pd.read_csv(path)
    _validate_columns(df, CONNECTIONS_REQUIRED_COLUMNS, str(path))
    return df


def load_classification(path: Path | str) -> pd.DataFrame:
    df = pd.read_csv(path)
    _validate_columns(df, CLASSIFICATION_REQUIRED_COLUMNS, str(path))
    return df


def load_raw_data(data_dir: Path | str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load connections.csv + classification.csv from a directory (raw Codex export or fixtures)."""
    data_dir = Path(data_dir)
    connections = load_connections(data_dir / "connections.csv")
    classification = load_classification(data_dir / "classification.csv")
    return connections, classification
