"""Compare healthy vs. damaged simulation runs and report % deviation in signal delay."""

from typing import NamedTuple

import networkx as nx
import pandas as pd

from mbsim.damage import (
    SlowdownFn,
    ThresholdFn,
    damaged_conduction_velocity,
    damaged_threshold,
    linear_slowdown,
    linear_threshold_increase,
)
from mbsim.perturbations import per_edge_velocity_severity, per_node_threshold_severity
from mbsim.simulation import simulate


class CompareResult(NamedTuple):
    df: pd.DataFrame
    summary: dict
    healthy_fire_times: dict[str, float]
    damaged_fire_times: dict[str, float]


def compare(
    graph: nx.DiGraph,
    input_nodes: list[str],
    output_nodes: list[str],
    base_conduction_velocity: float = 1.0,
    threshold: float = 1.0,
    perturbations: list[dict] | None = None,
    slowdown_fn: SlowdownFn = linear_slowdown,
    threshold_fn: ThresholdFn = linear_threshold_increase,
) -> CompareResult:
    """Healthy vs. damaged comparison, where `perturbations` (the same
    Tau/Amyloid/GABA/APL stack the UI's "+ Add Perturbation" panel builds) is
    resolved per-edge/per-node via `mbsim.perturbations`/`mbsim.targeting`
    instead of one global severity number — see those modules for why Tau and
    Amyloid default to every edge while GABA/APL only affect the specific
    edges/neurons they can actually be tied to in the connectome data.
    """
    perturbations = perturbations or []
    healthy_fire_times = simulate(graph, input_nodes, base_conduction_velocity, threshold)

    edge_severity = per_edge_velocity_severity(graph, perturbations)
    node_severity = per_node_threshold_severity(graph, perturbations)
    edge_velocity = {
        edge: damaged_conduction_velocity(base_conduction_velocity, severity, slowdown_fn)
        for edge, severity in edge_severity.items()
    }
    node_threshold = {
        node: damaged_threshold(threshold, severity, threshold_fn)
        for node, severity in node_severity.items()
    }
    damaged_fire_times = simulate(
        graph,
        input_nodes,
        base_conduction_velocity,
        threshold,
        edge_velocity=edge_velocity,
        node_threshold=node_threshold,
    )

    rows = []
    for node in output_nodes:
        healthy_t = healthy_fire_times.get(node)
        damaged_t = damaged_fire_times.get(node)
        if healthy_t is None or damaged_t is None:
            continue
        pct_deviation = ((damaged_t - healthy_t) / healthy_t * 100) if healthy_t > 0 else float("nan")
        rows.append(
            {
                "node": node,
                "healthy_time": healthy_t,
                "damaged_time": damaged_t,
                "pct_deviation": pct_deviation,
            }
        )

    df = pd.DataFrame(rows, columns=["node", "healthy_time", "damaged_time", "pct_deviation"])
    damaged_velocities = list(edge_velocity.values())
    damaged_thresholds = list(node_threshold.values())
    summary = {
        "base_conduction_velocity": base_conduction_velocity,
        "base_threshold": threshold,
        "n_edges_total": graph.number_of_edges(),
        "n_edges_velocity_targeted": len(edge_severity),
        "n_nodes_total": graph.number_of_nodes(),
        "n_nodes_threshold_targeted": len(node_severity),
        "mean_targeted_damaged_velocity": (
            sum(damaged_velocities) / len(damaged_velocities) if damaged_velocities else None
        ),
        "mean_targeted_damaged_threshold": (
            sum(damaged_thresholds) / len(damaged_thresholds) if damaged_thresholds else None
        ),
        "n_output_nodes_reached": len(df),
        "n_output_nodes_total": len(output_nodes),
        "mean_pct_deviation": df["pct_deviation"].mean() if not df.empty else None,
        "median_pct_deviation": df["pct_deviation"].median() if not df.empty else None,
    }
    return CompareResult(df, summary, healthy_fire_times, damaged_fire_times)


def plot_comparison(df: pd.DataFrame, out_path: str) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 4.5))
    x = range(len(df))
    width = 0.35
    ax.bar([i - width / 2 for i in x], df["healthy_time"], width, label="Healthy")
    ax.bar([i + width / 2 for i in x], df["damaged_time"], width, label="Damaged")
    ax.set_xticks(list(x))
    ax.set_xticklabels(df["node"], rotation=45, ha="right")
    ax.set_ylabel("Signal arrival time")
    ax.set_title("Mushroom Body output signal delay: healthy vs. damaged")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)
