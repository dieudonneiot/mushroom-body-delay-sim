"""Physical conduction delay -> Weber-Fechner subjective time-perception deviation.

Placeholder model, in the same spirit as `damage.py`: the Weber-Fechner law
(perceived magnitude scales with the logarithm of physical magnitude) is
applied to time perception as `perceived(t) = k * ln(1 + t / t0)`.

The damaged network's conduction is slower by a factor
`delay_ratio = damaged_delay_ms / healthy_delay_ms`. That ratio is applied as
a *horizontal* stretch of the time axis — the damaged curve at physical time
`t` reads as `perceived(t / delay_ratio)` — rather than a vertical rescale of
`k`. This means the damaged network needs `delay_ratio` times as much
physical time to register the same perceived magnitude the healthy network
registers at `t`, i.e. it under-registers elapsed duration in exactly the
direction the project's clinical example describes (an Alzheimer's patient
perceiving time as passing more slowly, so they wait longer than the target
interval before responding).

Critically, this makes `pct_deviation` here `(delay_ratio - 1) * 100`, i.e.
*exactly* `(damaged_delay_ms - healthy_delay_ms) / healthy_delay_ms * 100` —
the same figure, and the same formula, `mbsim.metrics.compare` reports as
`pct_deviation` for the simulated network. An earlier version of this module
instead rescaled `k` vertically (`k_damaged = k_healthy * healthy/damaged`),
which produced a numerically different deviation percentage from the one
shown elsewhere in the UI for the same run (e.g. 23.1% here vs. 30% there for
a 5.0ms->6.5ms case) — same underlying comparison, two disagreeing numbers.
The horizontal-stretch formulation removes that disagreement by
construction, not by coincidence.

This curve shape is still a documented assumption, not a literature-derived
result — swap in a real calibration (from Phase 2 lab data or the clinical
time-perception task) once available, without changing the shape of
`time_perception_deviation`'s return value.
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
    plus the delay-ratio deviation between them as a percentage — identical in
    formula to `mbsim.metrics.compare`'s `pct_deviation` (see module docstring).

    Returns `{"t", "healthy", "damaged", "pct_deviation"}`. Falls back to a flat
    zero curve and 0% deviation if either delay is non-positive (shouldn't happen
    via the UI, but keeps the function total).
    """
    t = np.logspace(np.log10(t_min), np.log10(t_max), n)

    if healthy_delay_ms <= 0 or damaged_delay_ms <= 0:
        zeros = np.zeros_like(t)
        return {"t": t, "healthy": zeros, "damaged": zeros, "pct_deviation": 0.0}

    delay_ratio = damaged_delay_ms / healthy_delay_ms
    healthy_curve = weber_fechner_curve(t, K_HEALTHY)
    damaged_curve = weber_fechner_curve(t / delay_ratio, K_HEALTHY)

    pct_deviation = (delay_ratio - 1.0) * 100.0

    return {"t": t, "healthy": healthy_curve, "damaged": damaged_curve, "pct_deviation": pct_deviation}
