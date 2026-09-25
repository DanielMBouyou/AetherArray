"""Acceptance thresholds, and an honest account of which ones exist.

**No threshold in this file is invented here.** A threshold either cites the
document that fixed it, or it is ``None`` and every verdict computed against it
comes back ``unresolved``.

That matters because a comparison tool that prints PASS against a number
somebody made up is worse than one that prints nothing: it manufactures
confidence. The repository currently records thresholds for the acquisition
path, in EXP-005, and **none at all for agreement between the electromagnetic
solver, the circuit simulator and the analyser.** Those are listed below as
unresolved so the gap is visible rather than silently filled.
"""
from __future__ import annotations

from dataclasses import dataclass

UNRESOLVED = "unresolved"
PASS = "pass"
FAIL = "fail"


@dataclass(frozen=True)
class Threshold:
    """A limit, its origin, and what to do when it does not exist yet."""

    key: str
    value: float | None
    unit: str
    source: str | None
    note: str

    def verdict(self, measured: float | None) -> str:
        if self.value is None or measured is None:
            return UNRESOLVED
        return PASS if abs(measured) <= self.value else FAIL

    def describe(self) -> str:
        if self.value is None:
            return f"{self.key}: no limit recorded ({self.note})"
        return f"{self.key}: {self.value} {self.unit} (from {self.source})"


#: Every threshold the comparison can apply. Add a value here **only** with a
#: source, and record that source in the document that fixed it.
THRESHOLDS: dict[str, Threshold] = {
    "s21_mag_diff_db": Threshold(
        key="s21_mag_diff_db",
        value=None,
        unit="dB",
        source=None,
        note="no agreement limit between solver, circuit simulator and analyser is "
        "recorded anywhere in this repository",
    ),
    "s21_phase_diff_deg": Threshold(
        key="s21_phase_diff_deg",
        value=None,
        unit="deg",
        source=None,
        note="as above; EXP-011 compares simulated against measured coupling but "
        "fixes no acceptance limit",
    ),
    "s11_mag_diff_db": Threshold(
        key="s11_mag_diff_db",
        value=None,
        unit="dB",
        source=None,
        note="as above",
    ),
    "amplitude_imbalance_db": Threshold(
        key="amplitude_imbalance_db",
        value=None,
        unit="dB",
        source=None,
        note="channel imbalance is a measured quantity in the benchmark contract, "
        "not a specification; no limit has been set",
    ),
    "channel_phase_spread_deg": Threshold(
        key="channel_phase_spread_deg",
        value=None,
        unit="deg",
        source=None,
        note="no limit set. The quantisation study in docs/mathematics/formulation.md "
        "describes the effect of phase error but does not fix an acceptance bound",
    ),
}


def get(key: str) -> Threshold:
    if key not in THRESHOLDS:
        raise KeyError(
            f"no threshold named {key!r}; add one with a source rather than inline"
        )
    return THRESHOLDS[key]


def unresolved_keys() -> list[str]:
    """Thresholds that still need a decision recorded somewhere in the repository."""
    return sorted(k for k, t in THRESHOLDS.items() if t.value is None)
