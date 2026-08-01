"""Simulated time units -> real milliseconds.

The event-driven simulation (`mbsim.simulation`) runs in an abstract time
unit derived from `edge_delay = 1 / (conduction_velocity * syn_count)` — that
unit has no inherent real-world scale. This module is the single place that
maps it to milliseconds, so the "Physical Conduction Delay" panel and any
downstream Weber-Fechner analysis report a number with one documented
source, instead of a bare user-typed multiplier with a magic default.

`ms_per_time_unit()` is currently one placeholder constant, loosely anchored
to literature figures for chemical synaptic delay in insects
(~1-2 ms/synapse) rather than a bare arbitrary number — but it is still NOT a
measurement, and should not be reported as one. Replace this function's body
(not just call sites) once real timing data exists to calibrate against —
the most direct source would be Phase 2 lab measurements (negative
geotaxis reaction time, or ideally electrophysiological recording of an
actual PN->KC->MBON transit time) landing in `data/lab/` (see
`data/lab/README.md`), or an equivalent literature figure the medical team
supplies. The UI's "Calibration" panel still allows a manual override on top
of this default for quick what-if exploration — that override never becomes
the default here.
"""

DEFAULT_MS_PER_TIME_UNIT = 5.0


def ms_per_time_unit() -> float:
    """Current best estimate of the simulated-time-unit -> millisecond scale.

    A placeholder (see module docstring), not a literature- or lab-derived
    value yet.
    """
    return DEFAULT_MS_PER_TIME_UNIT
