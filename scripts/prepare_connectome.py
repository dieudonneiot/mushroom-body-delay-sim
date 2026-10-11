"""Create the small app bundle from manually downloaded Codex CSV exports.

Usage:
    python scripts/prepare_connectome.py \
        data/raw/connections_princeton.csv.gz \
        data/raw/classification.csv.gz

Only ALPN, Kenyon_Cell, and MBON neurons and connections whose two endpoints
are in those groups are retained. Optional nt_type and neuropil fields are
preserved for the app's perturbation controls.
"""

from __future__ import annotations

import argparse
import csv
import gzip
from pathlib import Path
from typing import TextIO


ROLE_TYPES = {"ALPN", "Kenyon_Cell", "MBON"}
APP_DATA_DIR = Path("data/connectome")


def open_csv(path: Path) -> TextIO:
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8-sig", newline="")
    return path.open("r", encoding="utf-8-sig", newline="")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("connections", type=Path)
    parser.add_argument("classification", type=Path)
    parser.add_argument("--output-dir", type=Path, default=APP_DATA_DIR)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    classification_out = args.output_dir / "classification.csv"
    connections_out = args.output_dir / "connections.csv"

    selected_ids: set[str] = set()
    class_counts = {cell_type: 0 for cell_type in sorted(ROLE_TYPES)}
    with open_csv(args.classification) as source, classification_out.open(
        "w", encoding="utf-8", newline=""
    ) as destination:
        reader = csv.DictReader(source)
        if not {"root_id", "class"}.issubset(reader.fieldnames or []):
            raise ValueError("Classification CSV must have root_id and class columns")
        writer = csv.DictWriter(destination, fieldnames=["root_id", "class"])
        writer.writeheader()
        for row in reader:
            cell_type = row["class"]
            if cell_type in ROLE_TYPES:
                selected_ids.add(row["root_id"])
                class_counts[cell_type] += 1
                writer.writerow({"root_id": row["root_id"], "class": cell_type})

    if not selected_ids:
        raise ValueError("No ALPN, Kenyon_Cell, or MBON rows found in classification CSV")

    edge_count = 0
    with open_csv(args.connections) as source, connections_out.open(
        "w", encoding="utf-8", newline=""
    ) as destination:
        reader = csv.DictReader(source)
        required = {"pre_root_id", "post_root_id", "syn_count"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError("Connections CSV is missing required root ID/syn_count columns")
        columns = [name for name in ("pre_root_id", "post_root_id", "syn_count", "neuropil", "nt_type") if name in (reader.fieldnames or [])]
        writer = csv.DictWriter(destination, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for row in reader:
            if row["pre_root_id"] in selected_ids and row["post_root_id"] in selected_ids:
                writer.writerow(row)
                edge_count += 1

    print(f"Wrote {len(selected_ids):,} neurons to {classification_out}")
    print(f"Cell types: {class_counts}")
    print(f"Wrote {edge_count:,} pathway connections to {connections_out}")


if __name__ == "__main__":
    main()
