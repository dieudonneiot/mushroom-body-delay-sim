"""Named biological impairments -> combined disease severity.

This is the multi-factor extension point sitting in front of `damage.py`:
instead of one generic "severity" knob, the UI lets a user stack several
named perturbations (Tau protein, Beta-Amyloid, GABA dysfunction, APL neuron
impairment), each with its own 0-100% intensity. Each factor type has its own
placeholder `reduction_fn` (intensity fraction -> velocity-reduction
contribution), exactly like `damage.py::linear_slowdown` — swap any of them
for a literature-derived curve without touching the rest of the pipeline.

The combination rule turning several active contributions into the single
severity value `damage.py` expects is also a placeholder: independent
multiplicative combination (`1 - prod(1 - contribution_i)`), the standard way
to combine independent partial impairments so the result naturally stays in
[0, 1) regardless of how many factors are stacked. Replace with a
literature-derived interaction model (e.g. synergistic Tau/Amyloid effects)
once available.
"""

from typing import Callable

ReductionFn = Callable[[float], float]


def _clamped_identity(intensity_fraction: float) -> float:
    """Placeholder: contribution scales linearly with intensity in [0, 1]."""
    return max(0.0, min(1.0, intensity_fraction))


PERTURBATION_TYPES: dict[str, dict] = {
    "tau": {
        "label_key": "perturbation_tau",
        "description_key": "perturbation_tau_desc",
        "reduction_fn": _clamped_identity,
    },
    "amyloid": {
        "label_key": "perturbation_amyloid",
        "description_key": "perturbation_amyloid_desc",
        "reduction_fn": _clamped_identity,
    },
    "gaba": {
        "label_key": "perturbation_gaba",
        "description_key": "perturbation_gaba_desc",
        "reduction_fn": _clamped_identity,
    },
    "apl": {
        "label_key": "perturbation_apl",
        "description_key": "perturbation_apl_desc",
        "reduction_fn": _clamped_identity,
    },
}


def combined_severity(perturbations: list[dict]) -> float:
    """Combine active perturbations (each `{"type": str, "intensity": float 0-100}`)
    into a single severity value in [0, 1) for `damage.damaged_conduction_velocity`.

    Unknown types and non-positive intensities are ignored. Returns 0.0 for an
    empty/all-zero list (no perturbation = healthy baseline).
    """
    surviving_fraction = 1.0
    for perturbation in perturbations:
        ptype = PERTURBATION_TYPES.get(perturbation.get("type"))
        if ptype is None:
            continue
        intensity = perturbation.get("intensity", 0.0)
        if intensity <= 0:
            continue
        contribution = ptype["reduction_fn"](intensity / 100.0)
        surviving_fraction *= 1.0 - contribution
    return 1.0 - surviving_fraction
