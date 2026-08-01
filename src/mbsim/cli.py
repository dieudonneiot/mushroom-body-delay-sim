"""End-to-end pipeline runner: data -> MB subgraph -> graph -> healthy/damaged comparison."""

import argparse
from pathlib import Path

import yaml

from mbsim.graph import build_graph, print_sanity_report
from mbsim.io import load_raw_data
from mbsim.metrics import compare, plot_comparison
from mbsim.mushroom_body import extract_mb_subgraph
from mbsim.visualize import plot_network_delay, plot_network_structure


def run(config_path: str) -> None:
    config = yaml.safe_load(Path(config_path).read_text())

    data_cfg = config["data"]
    data_dir = data_cfg["raw_dir"] if data_cfg["mode"] == "raw" else data_cfg["fixture_dir"]
    connections, classification = load_raw_data(data_dir)

    damage_cfg = config["damage"]
    perturbations = damage_cfg.get("perturbations", [])
    # Every perturbation's target_root_ids (currently only APL uses this) must be
    # force-included, or targeting.resolve_targets would never see that neuron's
    # edges — see mushroom_body.py's extra_node_ids parameter.
    extra_node_ids = sorted({rid for p in perturbations for rid in p.get("target_root_ids", [])})

    edge_df, node_roles = extract_mb_subgraph(
        connections, classification, config["roles"], extra_node_ids=extra_node_ids
    )
    graph = build_graph(edge_df, node_roles)
    print_sanity_report(graph)

    input_nodes = [n for n, r in node_roles.items() if r == "input" and n in graph]
    output_nodes = [n for n, r in node_roles.items() if r == "output" and n in graph]
    if not input_nodes or not output_nodes:
        raise ValueError(
            f"Need at least one input and one output node in the graph; "
            f"got {len(input_nodes)} input, {len(output_nodes)} output."
        )

    sim_cfg = config["simulation"]
    result = compare(
        graph,
        input_nodes,
        output_nodes,
        base_conduction_velocity=sim_cfg["conduction_velocity"],
        threshold=sim_cfg["threshold"],
        perturbations=perturbations,
    )

    out_dir = Path(config["output"]["dir"])
    out_dir.mkdir(parents=True, exist_ok=True)
    result.df.to_csv(out_dir / "comparison.csv", index=False)
    if not result.df.empty:
        plot_comparison(result.df, str(out_dir / "comparison.png"))

    plot_network_structure(graph, str(out_dir / "network_structure.png"))
    plot_network_delay(
        graph,
        result.healthy_fire_times,
        str(out_dir / "network_healthy.png"),
        title="Signal arrival time — healthy network",
    )
    plot_network_delay(
        graph,
        result.damaged_fire_times,
        str(out_dir / "network_damaged.png"),
        title=(
            f"Signal arrival time — damaged network "
            f"({result.summary['n_edges_velocity_targeted']}/{result.summary['n_edges_total']} edges velocity-targeted, "
            f"{result.summary['n_nodes_threshold_targeted']}/{result.summary['n_nodes_total']} nodes threshold-targeted)"
        ),
    )

    print("\nHealthy vs. damaged signal delay at output (MBON) nodes:")
    print(result.df.to_string(index=False))
    print("\nSummary:")
    for key, value in result.summary.items():
        print(f"  {key}: {value}")
    print(f"\nResults written to {out_dir}/")


def main() -> None:
    parser = argparse.ArgumentParser(description="Mushroom Body signal-delay simulation")
    parser.add_argument(
        "--config", default="configs/default.yaml", help="Path to a YAML config file"
    )
    args = parser.parse_args()
    run(args.config)


if __name__ == "__main__":
    main()
