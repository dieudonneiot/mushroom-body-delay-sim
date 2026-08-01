"""Disease-severity -> conduction-velocity slowdown / firing-threshold increase.

This is the extension point for the medical team: swap `linear_slowdown` or
`linear_threshold_increase` for a literature-derived function without
touching `simulation.py`. There are two independent channels, fed by
different perturbation types (see `perturbations.py`):

- Velocity channel (Tau, Amyloid): takes a severity value (whatever scale
  the literature uses, e.g. 0-1 or a Braak stage) and returns the fraction
  by which conduction velocity is reduced (0 = no effect, 1 = fully
  blocked).
- Threshold channel (GABA, APL): takes a severity value and returns the
  fraction by which the firing threshold is *increased*. This models
  disinhibition as a noisier baseline that a real signal must now clear by
  a wider margin to be counted — a documented modeling assumption (see
  `perturbations.py`'s module docstring), not a literature-derived
  mechanism. Replace once the medical team specifies the real
  direction/magnitude.
"""

from typing import Callable

SlowdownFn = Callable[[float], float]
ThresholdFn = Callable[[float], float]


def linear_slowdown(severity: float) -> float:
    """Placeholder: velocity reduction scales linearly with severity in [0, 1].

    Replace with a real literature-derived curve once the medical team provides one.
    """
    return max(0.0, min(1.0, severity))


def linear_threshold_increase(severity: float) -> float:
    """Placeholder: firing-threshold increase scales linearly with severity in [0, 1]
    (0 = no change, 1 = threshold doubles).

    Replace with a real literature-derived curve once the medical team provides one.
    """
    return max(0.0, min(1.0, severity))


def damaged_conduction_velocity(
    base_conduction_velocity: float,
    severity: float,
    slowdown_fn: SlowdownFn = linear_slowdown,
) -> float:
    reduction = slowdown_fn(severity)
    return base_conduction_velocity * (1.0 - reduction)


def damaged_threshold(
    base_threshold: float,
    severity: float,
    threshold_fn: ThresholdFn = linear_threshold_increase,
) -> float:
    increase = threshold_fn(severity)
    return base_threshold * (1.0 + increase)
