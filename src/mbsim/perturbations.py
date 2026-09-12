"""Named biological impairments -> per-edge / per-node disease severity.

This is the multi-factor extension point sitting in front of `damage.py`:
instead of one generic "severity" knob, the UI lets a user stack several
named perturbations (Tau protein, Beta-Amyloid, GABA dysfunction, APL neuron
impairment), each with its own 0-100% intensity — and, since v2 of this
module, each restricted to the specific subset of edges/nodes it plausibly
affects (see `targeting.py`) rather than applied as one number to the whole
graph.

Each perturbation type declares which damage *channel* it feeds:
- "velocity": Tau and Amyloid disrupt axonal transport / synaptic
  transmission directly, so they reduce conduction velocity
  (`damage.damaged_conduction_velocity`) on their targeted edges.
- "threshold": GABA and APL loss are disinhibition mechanisms — losing
  their inhibitory tone raises baseline circuit noise rather than slowing
  transmission, so they raise the effective firing threshold
  (`damage.damaged_threshold`) at the postsynaptic end of their targeted
  edges, modeling a signal that must now clear a noisier baseline to be
  counted.

Each factor type has its own placeholder `reduction_fn` (intensity fraction
-> per-edge/per-node severity contribution), exactly like `damage.py`'s
slowdown/threshold functions — swap any of them for a literature-derived
curve without touching the rest of the pipeline, the other channel, or the
targeting logic.

Where several perturbations target the same edge/node, their contributions
combine via independent multiplicative combination
(`1 - prod(1 - contribution_i)`), the standard way to combine independent
partial impairments so the result naturally stays in [0, 1] regardless of
how many factors overlap there. Replace with a literature-derived
interaction model (e.g. synergistic Tau/Amyloid effects) once available.
"""

from typing import Callable

import networkx as nx

from mbsim.targeting import DEFAULT_TARGET_FNS, resolve_targets

ReductionFn = Callable[[float], float]

VELOCITY_CHANNEL = "velocity"
THRESHOLD_CHANNEL = "threshold"
CHANNELS = (VELOCITY_CHANNEL, THRESHOLD_CHANNEL)


def _clamped_identity(intensity_fraction: float) -> float:
    """Placeholder: contribution scales linearly with intensity in [0, 1]."""
    return max(0.0, min(1.0, intensity_fraction))


PERTURBATION_TYPES: dict[str, dict] = {
    "tau": {
        "label_key": "perturbation_tau",
        "description_key": "perturbation_tau_desc",
        "channel": VELOCITY_CHANNEL,
        "reduction_fn": _clamped_identity,
    },
    "amyloid": {
        "label_key": "perturbation_amyloid",
        "description_key": "perturbation_amyloid_desc",
        "channel": VELOCITY_CHANNEL,
        "reduction_fn": _clamped_identity,
    },
    "gaba": {
        "label_key": "perturbation_gaba",
        "description_key": "perturbation_gaba_desc",
        "channel": THRESHOLD_CHANNEL,
        "reduction_fn": _clamped_identity,
    },
    "apl": {
        "label_key": "perturbation_apl",
        "description_key": "perturbation_apl_desc",
        "channel": THRESHOLD_CHANNEL,
        "reduction_fn": _clamped_identity,
    },
}

# `targeting.DEFAULT_TARGET_FNS` must have an entry (possibly `None`, meaning
# "no default scope") for every type registered here — otherwise a type added
# to only one of the two dicts would still show up as a fully working,
# selectable UI perturbation, but silently resolve to zero targeted
# edges/nodes everywhere, indistinguishable from GABA/APL's legitimate no-op
# cases. Fail loudly at import time instead.
_unregistered_in_targeting = set(PERTURBATION_TYPES) - set(DEFAULT_TARGET_FNS)
if _unregistered_in_targeting:
    raise ImportError(
        f"Perturbation type(s) {sorted(_unregistered_in_targeting)} are in "
        "perturbations.PERTURBATION_TYPES but have no entry in "
        "targeting.DEFAULT_TARGET_FNS — add one (or explicitly None for "
        "'no default target') before using this type."
    )


def _active_contributions(perturbations: list[dict], channel: str):
    """Yield (contribution, targeted_edges) for every perturbation on `channel`
    with a known type and positive intensity."""
    for perturbation in perturbations:
        ptype = PERTURBATION_TYPES.get(perturbation.get("type"))
        if ptype is None or ptype["channel"] != channel:
            continue
        intensity = perturbation.get("intensity", 0.0)
        if intensity <= 0:
            continue
        yield perturbation, ptype, ptype["reduction_fn"](intensity / 100.0)


def per_edge_velocity_severity(graph: nx.DiGraph, perturbations: list[dict]) -> dict[tuple, float]:
    """{edge: severity in [0, 1]} for every edge touched by at least one active
    velocity-channel (Tau/Amyloid) perturbation. Edges untouched by any such
    perturbation are simply absent from the returned dict (severity 0, i.e.
    healthy)."""
    surviving: dict[tuple, float] = {}
    for perturbation, ptype, contribution in _active_contributions(perturbations, VELOCITY_CHANNEL):
        for edge in resolve_targets(graph, perturbation):
            surviving[edge] = surviving.get(edge, 1.0) * (1.0 - contribution)
    return {edge: 1.0 - fraction for edge, fraction in surviving.items()}


def per_node_threshold_severity(graph: nx.DiGraph, perturbations: list[dict]) -> dict[str, float]:
    """{node: severity in [0, 1]} for every postsynaptic node touched by at
    least one active threshold-channel (GABA/APL) perturbation. Nodes with no
    such incoming edge are absent from the returned dict (severity 0, i.e.
    healthy)."""
    surviving: dict[str, float] = {}
    for perturbation, ptype, contribution in _active_contributions(perturbations, THRESHOLD_CHANNEL):
        affected_nodes = {v for _, v in resolve_targets(graph, perturbation)}
        for node in affected_nodes:
            surviving[node] = surviving.get(node, 1.0) * (1.0 - contribution)
    return {node: 1.0 - fraction for node, fraction in surviving.items()}
