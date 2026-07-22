"""Event-driven signal propagation over the Mushroom Body graph.

A signal is injected at the configured input nodes at t=0 and propagates
edge-by-edge. Each edge has a transmission delay derived from its synapse
count and the current conduction velocity (the disease-severity knob lives
in `damage.py` and feeds into `conduction_velocity` here). A node "fires" the
first time it accumulates at least `threshold` worth of incoming signal, then
forwards a unit signal to its successors after each outgoing edge's delay.

This is intentionally a lightweight threshold/accumulation model rather than a
full biophysical spiking-neuron simulator: it's the simplest dynamic structure
that satisfies "runs when a signal is applied" while staying fast to build and
easy to reason about.
"""

import heapq
from collections import defaultdict

import networkx as nx


def edge_delay(syn_count: int, conduction_velocity: float) -> float:
    """More synapses (stronger connection) and higher conduction velocity -> shorter delay."""
    return 1.0 / (max(conduction_velocity, 1e-9) * max(syn_count, 1))


def simulate(
    graph: nx.DiGraph,
    input_nodes: list[str],
    conduction_velocity: float = 1.0,
    threshold: float = 1.0,
) -> dict[str, float]:
    """Return {node_id: first_fire_time} for every node reached by the signal."""
    accumulated: dict[str, float] = defaultdict(float)
    fire_time: dict[str, float] = {}
    heap: list[tuple[float, str, float]] = []

    for node in input_nodes:
        heapq.heappush(heap, (0.0, node, threshold))

    while heap:
        t, node, strength = heapq.heappop(heap)
        if node in fire_time:
            continue
        accumulated[node] += strength
        if accumulated[node] < threshold:
            continue
        fire_time[node] = t
        for successor in graph.successors(node):
            syn_count = graph.edges[node, successor]["weight"]
            delay = edge_delay(syn_count, conduction_velocity)
            heapq.heappush(heap, (t + delay, successor, 1.0))

    return fire_time
