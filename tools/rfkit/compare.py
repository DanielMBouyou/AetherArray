"""Comparing traces from different tools over the range they actually share."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field

import numpy as np

from . import thresholds as th
from .grid import Band, align, common_band
from .io import RfTrace
from .metrics import extract_at, mag_db, phase_error_deg, wrap_deg


@dataclass(frozen=True)
class PairComparison:
    """Agreement between two traces, at f0 and across the shared band."""

    a: str
    b: str
    f0_hz: float | None
    s21_mag_diff_db_at_f0: float | None
    s21_phase_diff_deg_at_f0: float | None
    s11_mag_diff_db_at_f0: float | None
    s21_mag_diff_db_max: float | None
    s21_mag_diff_db_rms: float | None
    s21_phase_diff_deg_max: float | None
    s21_phase_diff_deg_rms: float | None
    verdicts: dict = field(default_factory=dict)

    def as_dict(self) -> dict:
        return asdict(self)


def _rms(x: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(np.asarray(x, dtype=float)))))


def compare_pair(
    a: RfTrace,
    b: RfTrace,
    f0_hz: float | None = None,
    n_points: int | None = None,
) -> PairComparison:
    """Compare two traces.

    Both are aligned onto a grid inside their shared band first, so every
    number below is computed where both tools actually have data.
    """
    (aa, bb), grid = align([a, b], n_points=n_points)

    mag_max = mag_rms = ph_max = ph_rms = None
    if aa.n_ports >= 2 and bb.n_ports >= 2:
        d_mag = mag_db(aa.s(2, 1)) - mag_db(bb.s(2, 1))
        finite = np.isfinite(d_mag)
        if finite.any():
            mag_max = float(np.max(np.abs(d_mag[finite])))
            mag_rms = _rms(d_mag[finite])
        d_ph = phase_error_deg(
            np.degrees(np.angle(aa.s(2, 1))), np.degrees(np.angle(bb.s(2, 1)))
        )
        ph_max = float(np.max(np.abs(d_ph)))
        ph_rms = _rms(d_ph)

    m_at = p_at = s11_at = None
    if f0_hz is not None:
        ma, mb = extract_at(aa, f0_hz), extract_at(bb, f0_hz)
        if ma.s21_mag_db is not None and mb.s21_mag_db is not None:
            m_at = float(ma.s21_mag_db - mb.s21_mag_db)
        if ma.s21_phase_deg is not None and mb.s21_phase_deg is not None:
            p_at = float(wrap_deg(ma.s21_phase_deg - mb.s21_phase_deg))
        if ma.s11 is not None and mb.s11 is not None:
            da, db_ = mag_db(np.array([ma.s11]))[0], mag_db(np.array([mb.s11]))[0]
            # A perfectly matched port gives -inf dB. Subtracting two infinities
            # is not a small difference, it is undefined, so report nothing.
            s11_at = float(da - db_) if np.isfinite(da) and np.isfinite(db_) else None

    verdicts = {
        "s21_mag_diff_db": th.get("s21_mag_diff_db").verdict(mag_max),
        "s21_phase_diff_deg": th.get("s21_phase_diff_deg").verdict(ph_max),
        "s11_mag_diff_db": th.get("s11_mag_diff_db").verdict(s11_at),
    }
    return PairComparison(
        a=a.provenance.summary(),
        b=b.provenance.summary(),
        f0_hz=f0_hz,
        s21_mag_diff_db_at_f0=m_at,
        s21_phase_diff_deg_at_f0=p_at,
        s11_mag_diff_db_at_f0=s11_at,
        s21_mag_diff_db_max=mag_max,
        s21_mag_diff_db_rms=mag_rms,
        s21_phase_diff_deg_max=ph_max,
        s21_phase_diff_deg_rms=ph_rms,
        verdicts=verdicts,
    )


@dataclass
class ComparisonReport:
    """Everything a comparison run produced, ready to serialise."""

    band: Band
    grid_points: int
    f0_hz: float | None
    inputs: list = field(default_factory=list)
    pairs: list = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "band": {"start_hz": self.band.start_hz, "stop_hz": self.band.stop_hz},
            "grid_points": self.grid_points,
            "f0_hz": self.f0_hz,
            "inputs": [p.as_dict() for p in self.inputs],
            "pairs": [p.as_dict() for p in self.pairs],
            "unresolved_thresholds": th.unresolved_keys(),
        }

    def to_text(self) -> str:
        lines = ["AetherArray RF comparison", "=" * 26, ""]
        lines.append(f"shared band  : {self.band}")
        lines.append(f"grid points  : {self.grid_points}")
        lines.append(
            f"f0           : {self.f0_hz / 1e9:.6g} GHz" if self.f0_hz else "f0           : not requested"
        )
        lines += ["", "inputs", "------"]
        for p in self.inputs:
            lines.append(f"  {p.source:<9} {p.summary()}")
            lines.append(
                f"            {p.n_points} points, "
                f"{p.f_start_hz / 1e9:.4g} to {p.f_stop_hz / 1e9:.4g} GHz, "
                f"z0={p.z0_ohm:g}, cal={p.calibration}"
            )
        lines += ["", "pairwise agreement", "------------------"]
        for c in self.pairs:
            lines.append(f"  {c.a}  against  {c.b}")
            lines.append(
                f"    S21 magnitude difference : max "
                f"{_fmt(c.s21_mag_diff_db_max)} dB, rms {_fmt(c.s21_mag_diff_db_rms)} dB"
            )
            lines.append(
                f"    S21 phase difference     : max "
                f"{_fmt(c.s21_phase_diff_deg_max)} deg, rms {_fmt(c.s21_phase_diff_deg_rms)} deg"
            )
            if self.f0_hz:
                lines.append(
                    f"    at f0                    : "
                    f"{_fmt(c.s21_mag_diff_db_at_f0)} dB, {_fmt(c.s21_phase_diff_deg_at_f0)} deg"
                )
            for key, verdict in c.verdicts.items():
                lines.append(f"    {key:<24} : {verdict}")
        unresolved = th.unresolved_keys()
        if unresolved:
            lines += ["", "unresolved thresholds", "---------------------"]
            lines.append(
                "  These verdicts read 'unresolved' because no limit is recorded in"
            )
            lines.append("  the repository. That is a gap to close in a decision, not here.")
            for key in unresolved:
                lines.append(f"    {th.get(key).describe()}")
        return "\n".join(lines) + "\n"


def _fmt(x) -> str:
    return "n/a" if x is None else f"{x:.4g}"


def compare_all(
    traces: list[RfTrace],
    f0_hz: float | None = None,
    n_points: int | None = None,
) -> ComparisonReport:
    """Compare every pair of traces over the band they all share."""
    if len(traces) < 2:
        raise ValueError("need at least two traces to compare")
    band = common_band(traces)
    _, grid = align(traces, n_points=n_points)
    pairs = []
    for i in range(len(traces)):
        for j in range(i + 1, len(traces)):
            pairs.append(compare_pair(traces[i], traces[j], f0_hz=f0_hz, n_points=n_points))
    return ComparisonReport(
        band=band,
        grid_points=int(grid.size),
        f0_hz=f0_hz,
        inputs=[t.provenance for t in traces],
        pairs=pairs,
    )
