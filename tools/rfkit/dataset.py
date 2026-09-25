"""Repeated measurements, and the interface to the inverse calibration code.

Two jobs. First, statistics over repeated traces without losing the metadata
that makes them repeated measurements rather than a pile of numbers: session,
time, temperature. Second, the record the Bayesian inverse problem consumes.

The record fields follow ``docs/architecture/control-architecture.md`` section
6, which is the contract EXP-014 and EXP-015 write against.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

import numpy as np
import skrf

from .io import RfTrace
from .metrics import unwrapped_phase_deg, wrap_deg
from .provenance import Provenance

#: What a single observation is. The inverse problem's forward model differs
#: between them: complex is linear in the state, power is not.
OBSERVATION_KINDS = ("complex_s21", "power_dbm", "adc_counts")


@dataclass
class Measurement:
    """One observation, with everything needed to use it as evidence."""

    session: str
    sequence_index: int
    beam_state_word: int
    observation: complex | float
    observation_kind: str
    provenance: Provenance
    timestamp_counter: int | None = None
    wall_clock: str | None = None
    settling_s: float | None = None
    temperature_phase_c: float | None = None
    temperature_detector_c: float | None = None
    temperature_die_c: float | None = None
    raw_counts: list | None = None
    uncertainty: float | None = None
    uncertainty_kind: str | None = None
    gateware_version: str | None = None
    software_version: str | None = None
    connector_handled: bool | None = None

    def __post_init__(self) -> None:
        if self.observation_kind not in OBSERVATION_KINDS:
            raise ValueError(
                f"observation_kind must be one of {OBSERVATION_KINDS}, "
                f"got {self.observation_kind!r}"
            )
        if not 0 <= self.beam_state_word < 1 << 16:
            raise ValueError("beam_state_word is a 16 bit word")

    def channel_bits(self, channel: int) -> dict:
        """Decode one channel's nibble, per control architecture section 3.1.

        Bit ``b`` carries field ``f`` of channel ``c`` with ``b = 4c + f`` and
        the field order enable, 45, 90, 180.
        """
        base = 4 * channel
        names = ("enable", "b45", "b90", "b180")
        return {n: bool(self.beam_state_word >> (base + i) & 1) for i, n in enumerate(names)}

    def as_dict(self) -> dict:
        d = asdict(self)
        d["provenance"] = self.provenance.as_dict()
        if isinstance(self.observation, complex):
            d["observation"] = {"real": self.observation.real, "imag": self.observation.imag}
        return d


@dataclass
class MeasurementSet:
    """Repeated traces plus their metadata, kept side by side.

    ``skrf.NetworkSet`` gives the statistics. It does not carry session or
    temperature, so those live in a parallel list of the same length and are
    never flattened away.
    """

    traces: list = field(default_factory=list)
    records: list = field(default_factory=list)

    def add(self, trace: RfTrace, record: Measurement | None = None) -> None:
        self.traces.append(trace)
        self.records.append(record)

    def __len__(self) -> int:
        return len(self.traces)

    def network_set(self) -> skrf.NetworkSet:
        """The traces as a ``NetworkSet``, for the statistical operations.

        Every trace must already be on a common grid: see :func:`rfkit.grid.align`.
        This refuses rather than resampling silently, because resampling inside
        a statistics call is exactly where a hidden extrapolation would live.
        """
        if not self.traces:
            raise ValueError("empty set")
        f0 = self.traces[0].f
        for t in self.traces[1:]:
            if t.f.shape != f0.shape or not np.allclose(t.f, f0):
                raise ValueError(
                    "traces are not on a common grid; call rfkit.grid.align first"
                )
        return skrf.NetworkSet([t.network for t in self.traces])

    def mean_s21(self) -> np.ndarray:
        """Complex mean of S21 across the set, element by element in frequency."""
        return np.mean(np.stack([t.s(2, 1) for t in self.traces]), axis=0)

    def std_s21_db(self) -> np.ndarray:
        """Standard deviation of the S21 magnitude in dB, across the set."""
        mags = np.stack([20 * np.log10(np.abs(t.s(2, 1))) for t in self.traces])
        return np.std(mags, axis=0, ddof=1) if len(self.traces) > 1 else np.zeros(mags.shape[1])

    def std_s21_phase_deg(self) -> np.ndarray:
        """Standard deviation of S21 phase in degrees, computed on the circle.

        Phases are referred to the set's circular mean before the spread is
        taken, so a set sitting near the wrap point does not report 360 degrees
        of scatter.
        """
        vals = np.stack([t.s(2, 1) for t in self.traces])
        unit = vals / np.abs(vals)
        mean_angle = np.degrees(np.angle(np.mean(unit, axis=0)))
        errs = wrap_deg(np.degrees(np.angle(vals)) - mean_angle)
        return np.std(errs, axis=0, ddof=1) if len(self.traces) > 1 else np.zeros(errs.shape[1])

    def repeatability_summary(self, f_index: int | None = None) -> dict:
        """Spread across repeats, at one frequency point or across the sweep."""
        db, ph = self.std_s21_db(), self.std_s21_phase_deg()
        sl = slice(None) if f_index is None else slice(f_index, f_index + 1)
        return {
            "n_repeats": len(self.traces),
            "s21_mag_std_db_max": float(np.max(db[sl])),
            "s21_phase_std_deg_max": float(np.max(ph[sl])),
            "sessions": sorted({r.session for r in self.records if r is not None}),
            "temperatures_phase_c": [
                r.temperature_phase_c for r in self.records if r is not None
            ],
        }


def write_dataset(records: list, path: Path | str) -> None:
    """Write measurement records as newline delimited JSON.

    One record per line, so a long unattended run appends rather than rewrites,
    and a truncated file still parses up to the last complete line.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record.as_dict(), sort_keys=True) + "\n")


def read_dataset(path: Path | str) -> list:
    """Read back what :func:`write_dataset` wrote, as plain dictionaries."""
    out = []
    with open(Path(path), encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out
