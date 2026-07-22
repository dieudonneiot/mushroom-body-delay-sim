"""Disease-severity -> conduction-velocity slowdown.

This is the extension point for the medical team: swap `linear_slowdown` for a
literature-derived function without touching `simulation.py`. A slowdown
function takes a severity value (whatever scale the literature uses, e.g. 0-1
or a Braak stage) and returns the fraction by which conduction velocity is
reduced (0 = no effect, 1 = fully blocked).
"""

from typing import Callable

SlowdownFn = Callable[[float], float]


def linear_slowdown(severity: float) -> float:
    """Placeholder: velocity reduction scales linearly with severity in [0, 1].

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
