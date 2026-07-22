"""Compare healthy vs. damaged simulation runs and report % deviation in signal delay."""

from typing import NamedTuple

import networkx as nx
import pandas as pd

from mbsim.damage import SlowdownFn, damaged_conduction_velocity, linear_slowdown
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
    severity: float = 0.3,
    slowdown_fn: SlowdownFn = linear_slowdown,
) -> CompareResult:
    healthy_fire_times = simulate(graph, input_nodes, base_conduction_velocity, threshold)

    damaged_velocity = damaged_conduction_velocity(base_conduction_velocity, severity, slowdown_fn)
    damaged_fire_times = simulate(graph, input_nodes, damaged_velocity, threshold)

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
    summary = {
        "severity": severity,
        "base_conduction_velocity": base_conduction_velocity,
        "damaged_conduction_velocity": damaged_velocity,
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
