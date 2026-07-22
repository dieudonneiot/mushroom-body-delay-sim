"""Filter whole-brain connectome data down to the Mushroom Body pathway of interest.

Filtering is done purely by cell type role (e.g. PN / KC / MBON) rather than by
neuropil region string, since neuropil label formatting has varied across Codex
releases while cell-type classification is comparatively stable.
"""

import pandas as pd


def _invert_roles(roles: dict[str, list[str]]) -> dict[str, str]:
    """{"input": ["PN"], "relay": ["KC"]} -> {"PN": "input", "KC": "relay"}."""
    cell_type_to_role = {}
    for role, cell_types in roles.items():
        for cell_type in cell_types:
            cell_type_to_role[cell_type] = role
    return cell_type_to_role


def extract_mb_subgraph(
    connections: pd.DataFrame,
    classification: pd.DataFrame,
    roles: dict[str, list[str]],
) -> tuple[pd.DataFrame, dict[str, str]]:
    """Return (edge_df, node_roles) restricted to neurons whose cell_type is in `roles`.

    edge_df columns: pre_id, post_id, syn_count, pre_role, post_role.
    node_roles: {root_id: role_name} for every neuron kept.
    """
    cell_type_to_role = _invert_roles(roles)

    relevant = classification[classification["cell_type"].isin(cell_type_to_role)]
    node_roles = {
        row.root_id: cell_type_to_role[row.cell_type] for row in relevant.itertuples()
    }
    if not node_roles:
        raise ValueError(
            f"No neurons matched configured roles {roles}. "
            "Check that classification.csv cell_type values match the role config."
        )

    relevant_ids = set(node_roles)
    edges = connections[
        connections["pre_root_id"].isin(relevant_ids)
        & connections["post_root_id"].isin(relevant_ids)
    ].copy()

    edges = edges.rename(columns={"pre_root_id": "pre_id", "post_root_id": "post_id"})
    edges["pre_role"] = edges["pre_id"].map(node_roles)
    edges["post_role"] = edges["post_id"].map(node_roles)

    columns = ["pre_id", "post_id", "syn_count", "pre_role", "post_role"]
    return edges[columns].reset_index(drop=True), node_roles
