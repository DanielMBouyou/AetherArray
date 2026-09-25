"""Calibration and de-embedding interfaces.

**Nothing in this module has been performed.** No calibration kit has been
confirmed present, no fixture exists, no coupon has been fabricated and no
corrected measurement has been taken. Observation O7 in EXP-004 is the open
item, and open item H1 is not related but is equally unresolved.

The functions here therefore define the boundary and refuse to run. They exist
so that when standards arrive, the call sites are already correct and nothing
downstream has quietly assumed raw data was corrected.
"""
from __future__ import annotations

from dataclasses import dataclass

import skrf

from .io import RfTrace


class CalibrationNotAvailable(RuntimeError):
    """Raised when a correction is requested that no evidence supports."""


@dataclass(frozen=True)
class CalibrationPlan:
    """What a calibration would consist of, recorded before it exists."""

    method: str
    standards: tuple
    reference_plane: str
    note: str = ""

    def describe(self) -> str:
        return (
            f"{self.method} at {self.reference_plane} using "
            f"{', '.join(self.standards)}. {self.note}".strip()
        )


#: The plan implied by decision 0003 and the connector chain discussion in
#: ``docs/hardware/measurement-bench.md`` section 6. It is a plan, not a state.
SOLT_AT_ADAPTER_OUTPUT = CalibrationPlan(
    method="SOLT",
    standards=("short", "open", "load", "through"),
    reference_plane="the output of the N to 3.5 mm adapter, which is where the board mates",
    note="requires a kit and adapters, neither of which has been confirmed to exist",
)


def apply_calibration(trace: RfTrace, plan: CalibrationPlan = SOLT_AT_ADAPTER_OUTPUT):
    """Would apply a calibration. Refuses, because none exists.

    Kept as a named boundary so that call sites read correctly today and need
    no change when a kit is confirmed.
    """
    raise CalibrationNotAvailable(
        "no calibration has been performed. "
        f"Planned: {plan.describe()}. "
        "Observation O7 in EXP-004 has not established that a kit or adapters exist. "
        "Until it does, traces carry calibration='none' and must be reported as raw."
    )


def deembed(trace: RfTrace, fixture: skrf.Network):
    """Would remove a fixture from a measurement. Refuses, because none exists.

    When a fixture does exist, this wraps the scikit-rf primitives rather than
    reimplementing them.
    """
    raise CalibrationNotAvailable(
        "no fixture model exists, so nothing can be de-embedded. "
        "A fixture model requires either a measured coupon or a solver model of "
        "the launch, and neither has been produced."
    )


def assert_raw(trace: RfTrace) -> None:
    """Guard for code that must not silently consume corrected data."""
    if trace.provenance.calibration != "none":
        raise ValueError(
            f"expected raw data, got calibration={trace.provenance.calibration!r}"
        )


FUTURE_WORK = """
Deliberately out of scope for Rev A, recorded so the options are not rediscovered:

- A TRL coupon on the same panel as the board, which would give a reference plane
  at the launch without needing a commercial kit at that plane.
- IEEE P370 style de-embedding for the fixture, once a fixture exists.
- Time domain gating to separate the direct path from room echoes. Whether the
  analyser offers it is EXP-004 observation O8, and its absence is not a blocker.
- Vector fitting to obtain a rational model of a measured response, useful if a
  circuit level model of the chain is ever wanted.

None of these is a Rev A requirement, and none should become one without a
decision record saying why.
"""
