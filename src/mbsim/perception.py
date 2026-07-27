"""Physical conduction delay -> Weber-Fechner subjective time-perception deviation.

Placeholder model, in the same spirit as `damage.py`: the Weber-Fechner law
(perceived magnitude scales with the logarithm of physical magnitude) is
applied to time perception as `perceived(t) = k * ln(1 + t / t0)`. The
damaged network's conduction is slower, so its modeled internal-clock gain
`k_damaged` is scaled down proportionally to how much slower its physical
delay is relative to the healthy network's:

    k_damaged = k_healthy * (healthy_delay_ms / damaged_delay_ms)

This is a documented assumption, not a literature-derived result — swap in a
real calibration (from Phase 2 lab data or the clinical time-perception task)
once available, without changing the shape of `time_perception_deviation`'s
return value.
"""

import numpy as np

K_HEALTHY = 1.0
T0_SECONDS = 1.0


def weber_fechner_curve(t: np.ndarray, k: float, t0: float = T0_SECONDS) -> np.ndarray:
    """Perceived time under the Weber-Fechner law: k * ln(1 + t / t0)."""
    return k * np.log1p(np.asarray(t) / t0)


def time_perception_deviation(
    healthy_delay_ms: float,
    damaged_delay_ms: float,
    t_min: float = 0.1,
    t_max: float = 30.0,
    n: int = 200,
) -> dict:
    """Healthy vs. damaged Weber-Fechner curves over a physical-time range (seconds),
    plus the mean relative deviation between them as a percentage.

    Returns `{"t", "healthy", "damaged", "pct_deviation"}`. Falls back to a flat
    zero curve and 0% deviation if either delay is non-positive (shouldn't happen
    via the UI, but keeps the function total).
    """
    t = np.logspace(np.log10(t_min), np.log10(t_max), n)

    if healthy_delay_ms <= 0 or damaged_delay_ms <= 0:
        zeros = np.zeros_like(t)
        return {"t": t, "healthy": zeros, "damaged": zeros, "pct_deviation": 0.0}

    k_damaged = K_HEALTHY * (healthy_delay_ms / damaged_delay_ms)
    healthy_curve = weber_fechner_curve(t, K_HEALTHY)
    damaged_curve = weber_fechner_curve(t, k_damaged)

    pct_deviation = float(np.mean(np.abs(damaged_curve - healthy_curve) / healthy_curve) * 100)

    return {"t": t, "healthy": healthy_curve, "damaged": damaged_curve, "pct_deviation": pct_deviation}
