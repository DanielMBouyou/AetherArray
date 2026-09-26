"""Acceptance thresholds, where each one comes from, and which ones do not exist.

**No threshold in this file is invented here.** Every entry is one of three
kinds, and says which:

- ``provisional-theory-derived``: a value derived in :mod:`rfkit.budget` from
  its consequence at the array level, adopted by decision 0007, and recorded
  with the name of the function that reproduces it. The tests fail if the
  recorded value and the derivation part company. Provisional until the
  conditions in that decision are met.
- ``unresolved``: no value, because a term the derivation needs is not known.
  The note names the term. Every verdict against it reads ``unresolved``.
- ``not-a-limit``: deliberately no value, because a limit on this quantity would
  contradict the design. Every verdict reads ``not applicable``.

Thresholds are keyed by metric **and** by comparison class. The same metric has
different uncertainty sources in a design check, in a comparison of two
simulators, and in a comparison of a simulation with a measurement, so one
number for all three would be right for at most one of them.

A comparison tool that prints PASS against a number somebody made up is worse
than one that prints nothing: it manufactures confidence. That is still the
rule this file exists to keep.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass

from .budget import BAND_START_HZ, BAND_STOP_HZ, F0_HZ

# ----------------------------------------------------------------- verdicts
UNRESOLVED = "unresolved"
PASS = "pass"
FAIL = "fail"
NOT_APPLICABLE = "not applicable"

# ------------------------------------------------------------------ statuses
PROVISIONAL = "provisional-theory-derived"
STATUS_UNRESOLVED = "unresolved"
NOT_A_LIMIT = "not-a-limit"
STATUSES = (PROVISIONAL, STATUS_UNRESOLVED, NOT_A_LIMIT)

# --------------------------------------------------------- comparison classes
DESIGN = "design"
HFSS_VS_ADS = "hfss_vs_ads"
SIMULATION_VS_VNA = "simulation_vs_vna"
COMPARISON_CLASSES = (DESIGN, HFSS_VS_ADS, SIMULATION_VS_VNA)

# ------------------------------------------------ what a threshold applies to
#: One trace's value, or the plain difference between two traces.
ABSOLUTE = "absolute"
#: Each commanded state relative to a reference state, the part of a difference
#: the diagonal array state cannot absorb. See :func:`rfkit.compare.compare_states`.
STATE_DIFFERENTIAL = "state differential"
#: Across the channels of one array state.
CHANNEL_SPREAD = "channel spread"

DECISION = "decisions/0007-provisional-rf-acceptance-budget.md"

#: The single policy input: the fraction of the quantisation floor's error
#: variance that a discrepancy may add. A declared choice, recorded in decision
#: 0007. Every provisional value below is derived from it, and the tests check
#: that they still are.
VARIANCE_FRACTION = 0.10

#: Where the thresholds are judged: band 57a, decision 0004, and f0 inside it.
OPERATING_BAND_HZ = (BAND_START_HZ, BAND_STOP_HZ)
OPERATING_F0_HZ = F0_HZ


@dataclass(frozen=True)
class Threshold:
    """A limit, the quantity it applies to, its status, and where it came from."""

    key: str
    comparison: str
    value: float | None
    unit: str
    status: str
    quantity: str
    note: str
    source: str | None = None
    #: Name of the :mod:`rfkit.budget` function that reproduces ``value``.
    derivation: str | None = None

    def __post_init__(self) -> None:
        if self.status not in STATUSES:
            raise ValueError(f"unknown status {self.status!r}")
        if self.comparison not in COMPARISON_CLASSES:
            raise ValueError(f"unknown comparison class {self.comparison!r}")
        if self.status == PROVISIONAL:
            if self.value is None or not self.source or not self.derivation:
                raise ValueError(f"{self.id}: a value needs a source and a derivation")
        elif self.value is not None:
            raise ValueError(f"{self.id}: only a derived threshold may carry a value")
        if not self.note:
            raise ValueError(f"{self.id}: every threshold explains itself")

    @property
    def id(self) -> str:
        return f"{self.key}[{self.comparison}]"

    def verdict(self, measured: float | None) -> str:
        if self.status == NOT_A_LIMIT:
            return NOT_APPLICABLE
        if self.value is None or measured is None:
            return UNRESOLVED
        return PASS if abs(measured) <= self.value else FAIL

    def describe(self) -> str:
        if self.value is None:
            return f"{self.id}: no limit, {self.status} ({self.note})"
        return f"{self.id}: {self.value} {self.unit}, {self.status}, {self.quantity} (from {self.source})"

    def as_dict(self) -> dict:
        d = asdict(self)
        d["id"] = self.id
        return d


_PHASE_T = 2.29   # deg, derive_phase_agreement_deg(0.10) = 2.2964, rounded down
_MAG_T = 0.40     # dB, derive_magnitude_agreement_db(0.10, 2.29) = 0.4032, rounded down
_IMB_T = 0.82     # dB, derive_amplitude_imbalance_db(0.10, 2.29) = 0.8261, rounded down

_ALL = (
    Threshold(
        key="s21_phase_diff_deg", comparison=HFSS_VS_ADS, value=_PHASE_T, unit="deg",
        status=PROVISIONAL, quantity=STATE_DIFFERENTIAL,
        note="state dependent part of the S21 phase difference between the two "
        "simulators, each state against the reference state, largest over the "
        "operating band including f0. Bounds the worst pattern, so the pointing "
        "shift stays within sqrt(eta) of the quantisation floor",
        source=DECISION, derivation="derive_phase_agreement_deg",
    ),
    Threshold(
        key="s21_mag_diff_db", comparison=HFSS_VS_ADS, value=_MAG_T, unit="dB",
        status=PROVISIONAL, quantity=STATE_DIFFERENTIAL,
        note="state dependent part of the S21 magnitude difference, as for phase. "
        "Takes the gain and sidelobe budget the phase bound leaves, so the two "
        "limits hold jointly",
        source=DECISION, derivation="derive_magnitude_agreement_db",
    ),
    Threshold(
        key="s21_phase_diff_deg", comparison=SIMULATION_VS_VNA, value=None, unit="deg",
        status=STATUS_UNRESOLVED, quantity=STATE_DIFFERENTIAL,
        note=f"guarded acceptance: observed difference plus the analyser's expanded "
        f"uncertainty within {_PHASE_T} deg. That uncertainty at 2.44 GHz is unknown "
        "until the model is read, EXP-004 O1, and a calibration chain exists, O7",
    ),
    Threshold(
        key="s21_mag_diff_db", comparison=SIMULATION_VS_VNA, value=None, unit="dB",
        status=STATUS_UNRESOLVED, quantity=STATE_DIFFERENTIAL,
        note=f"guarded acceptance within {_MAG_T} dB, unresolved for the same "
        "reason: no analyser uncertainty at 2.44 GHz, EXP-004 O1 and O7",
    ),
    Threshold(
        key="s11_mag_diff_db", comparison=HFSS_VS_ADS, value=None, unit="dB",
        status=STATUS_UNRESOLVED, quantity=ABSOLUTE,
        note="no array level consequence in these units. Between 50 ohm ports the "
        "S21 comparison already carries the effect of mismatch, and the remaining "
        "interaction term needs the match of the divider outputs and the elements, "
        "which are not designed",
    ),
    Threshold(
        key="s11_mag_diff_db", comparison=SIMULATION_VS_VNA, value=None, unit="dB",
        status=STATUS_UNRESOLVED, quantity=ABSOLUTE,
        note="as for the two simulators, and the analyser uncertainty is also unknown",
    ),
    Threshold(
        key="amplitude_imbalance_db", comparison=DESIGN, value=_IMB_T, unit="dB",
        status=PROVISIONAL, quantity=CHANNEL_SPREAD,
        note="peak to peak magnitude spread of the diagonal state across channels. "
        "Phase only control cannot correct it, so it stays in the calibrated beam; "
        "bounded for its worst arrangement, jointly with a state error at the "
        "phase bound",
        source=DECISION, derivation="derive_amplitude_imbalance_db",
    ),
    Threshold(
        key="channel_phase_spread_deg", comparison=DESIGN, value=None, unit="deg",
        status=NOT_A_LIMIT, quantity=CHANNEL_SPREAD,
        note="deliberately no limit. A per channel phase offset is absorbed by the "
        "diagonal state and corrected modulo 360 by phase only control; this spread "
        "is what calibration exists to remove, and a limit on it would be a "
        "performance claim rather than an acceptance test",
    ),
)

#: Every threshold, keyed by ``(metric, comparison class)``.
THRESHOLDS: dict[tuple[str, str], Threshold] = {(t.key, t.comparison): t for t in _ALL}


def get(key: str, comparison: str) -> Threshold:
    if (key, comparison) not in THRESHOLDS:
        raise KeyError(
            f"no threshold named {key!r} for {comparison!r}; add one with a "
            "derivation and a source rather than inline"
        )
    return THRESHOLDS[(key, comparison)]


def all_thresholds() -> list[Threshold]:
    return list(_ALL)


def unresolved_keys() -> list[str]:
    """Thresholds that still need a term measured, as ``metric[class]``."""
    return sorted(t.id for t in _ALL if t.status == STATUS_UNRESOLVED)


def provisional() -> list[Threshold]:
    return [t for t in _ALL if t.status == PROVISIONAL]


def comparison_class(sources, explicit: str | None = None) -> str | None:
    """The comparison class of a set of provenance sources.

    ``hfss`` with ``ads`` is a comparison of simulators; either with ``vna`` is a
    simulation against a measurement. Anything else has no class here: two
    traces from one tool, or two analyser traces, is repeatability, which is
    EXP-005's subject and not this module's.

    A ``synthetic`` trace has no class of its own, and ``explicit`` says what it
    stands in for. That is how the tests exercise the verdicts **without ever
    labelling a formula as solver output**. An explicit class that contradicts
    real sources is an error, not an override.
    """
    s = set(sources)
    if explicit is not None and explicit not in COMPARISON_CLASSES:
        raise ValueError(f"unknown comparison class {explicit!r}")
    if "synthetic" in s:
        return explicit
    if s == {"hfss", "ads"}:
        inferred = HFSS_VS_ADS
    elif "vna" in s and len(s) == 2 and s - {"vna"} <= {"hfss", "ads"}:
        inferred = SIMULATION_VS_VNA
    else:
        inferred = None
    if explicit is not None and explicit != inferred:
        raise ValueError(
            f"sources {sorted(s)} are a {inferred!r} comparison, not {explicit!r}"
        )
    return inferred
