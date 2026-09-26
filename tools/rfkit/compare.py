"""Comparing traces from different tools over the range they actually share.

Two comparisons, because the downstream consequence lives in only one of them:

- :func:`compare_pair` reports the plain difference between two traces. Part
  of any such difference is common to every commanded state, and the diagonal
  array state absorbs it, so no derived limit applies to it. Its S21 verdicts
  read ``not applicable`` and point here.
- :func:`compare_states` takes the same channel in every state from two tools
  and keeps only the state dependent part of their difference, which is what a
  calibration cannot absorb and what the provisional thresholds bound.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field

import numpy as np

from . import thresholds as th
from .grid import Band, align, common_band, common_grid, interp_complex
from .io import RfTrace
from .metrics import extract_at, mag_db, phase_error_deg, wrap_deg


@dataclass(frozen=True)
class PairComparison:
    """Agreement between two traces, at f0 and across the shared band."""

    a: str
    b: str
    comparison: str | None
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


def _pair_verdict(key: str, comparison: str | None, measured: float | None, quantity: str) -> str:
    """Apply a threshold only to the quantity it was derived for."""
    if comparison is None:
        return th.UNRESOLVED
    t = th.get(key, comparison)
    if t.status != th.NOT_A_LIMIT and t.quantity != quantity:
        return th.NOT_APPLICABLE
    return t.verdict(measured)


def compare_pair(
    a: RfTrace,
    b: RfTrace,
    f0_hz: float | None = None,
    n_points: int | None = None,
    comparison: str | None = None,
) -> PairComparison:
    """Compare two traces.

    Both are aligned onto a grid inside their shared band first, so every
    number below is computed where both tools actually have data. The
    comparison class comes from the two sources; ``comparison`` is only for
    synthetic traces, see :func:`rfkit.thresholds.comparison_class`.
    """
    cls = th.comparison_class([a.provenance.source, b.provenance.source], comparison)
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
        "s21_mag_diff_db": _pair_verdict("s21_mag_diff_db", cls, mag_max, th.ABSOLUTE),
        "s21_phase_diff_deg": _pair_verdict("s21_phase_diff_deg", cls, ph_max, th.ABSOLUTE),
        "s11_mag_diff_db": _pair_verdict("s11_mag_diff_db", cls, s11_at, th.ABSOLUTE),
    }
    return PairComparison(
        a=a.provenance.summary(),
        b=b.provenance.summary(),
        comparison=cls,
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
            lines.append(f"  {c.a}  against  {c.b}  ({c.comparison or 'no comparison class'})")
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
        lines += _threshold_notes()
        return "\n".join(lines) + "\n"


def _threshold_notes() -> list[str]:
    lines = ["", "about the verdicts", "------------------"]
    lines.append("  not applicable : a plain difference between two traces includes a part")
    lines.append("                   common to every state, which the array state absorbs.")
    lines.append("                   The S21 limits apply to state differences; use")
    lines.append("                   compare_states, or the compare-states command.")
    lines.append("  unresolved     : no limit, because a term it needs is unknown:")
    for t in th.all_thresholds():
        if t.status == th.STATUS_UNRESOLVED:
            lines.append(f"    {t.id}")
    prov = th.provisional()
    if prov:
        lines.append("  provisional    : derived from the array level budget, decision 0007,")
        lines.append("                   not from data. Values in force:")
        for t in prov:
            lines.append(f"    {t.id} = {t.value} {t.unit}")
    return lines


def _fmt(x) -> str:
    return "n/a" if x is None else f"{x:.4g}"


def compare_all(
    traces: list[RfTrace],
    f0_hz: float | None = None,
    n_points: int | None = None,
    comparison: str | None = None,
) -> ComparisonReport:
    """Compare every pair of traces over the band they all share."""
    if len(traces) < 2:
        raise ValueError("need at least two traces to compare")
    band = common_band(traces)
    _, grid = align(traces, n_points=n_points)
    pairs = []
    for i in range(len(traces)):
        for j in range(i + 1, len(traces)):
            pairs.append(compare_pair(traces[i], traces[j], f0_hz=f0_hz,
                                      n_points=n_points, comparison=comparison))
    return ComparisonReport(
        band=band,
        grid_points=int(grid.size),
        f0_hz=f0_hz,
        inputs=[t.provenance for t in traces],
        pairs=pairs,
    )


# ------------------------------------------------------------ state by state
@dataclass
class StateComparison:
    """Two tools compared state by state, on what the array state cannot absorb."""

    a_source: str
    b_source: str
    comparison: str | None
    reference_state: int
    states: list
    band: Band
    band_covered: bool
    f0_hz: float
    points_judged: int
    phase_diff_deg_max: float | None
    mag_diff_db_max: float | None
    phase_diff_deg_at_f0: float | None
    mag_diff_db_at_f0: float | None
    per_state: dict = field(default_factory=dict)
    verdicts: dict = field(default_factory=dict)
    provenance: list = field(default_factory=list)

    def as_dict(self) -> dict:
        d = asdict(self)
        d["band"] = {"start_hz": self.band.start_hz, "stop_hz": self.band.stop_hz}
        return d

    def to_text(self) -> str:
        lines = ["AetherArray state by state comparison", "=" * 37, ""]
        lines.append(f"tools        : {self.a_source} against {self.b_source}"
                     f"  ({self.comparison or 'no comparison class'})")
        lines.append(f"states       : {self.states}, reference {self.reference_state}")
        lines.append(f"judged band  : {self.band}"
                     + ("" if self.band_covered else "  NOT COVERED, in band verdicts unresolved"))
        lines.append(f"points       : {self.points_judged}, including both edges and f0")
        lines += ["", "state dependent difference, largest over the band", "-" * 50]
        for s, v in self.per_state.items():
            lines.append(f"  state {s}: phase {_fmt(v['phase_deg_max'])} deg, "
                         f"magnitude {_fmt(v['mag_db_max'])} dB")
        lines.append(f"  all states: phase {_fmt(self.phase_diff_deg_max)} deg, "
                     f"magnitude {_fmt(self.mag_diff_db_max)} dB")
        lines.append(f"  at f0     : phase {_fmt(self.phase_diff_deg_at_f0)} deg, "
                     f"magnitude {_fmt(self.mag_diff_db_at_f0)} dB")
        lines += ["", "verdicts", "--------"]
        for key, verdict in self.verdicts.items():
            lines.append(f"  {key:<24} : {verdict}")
        lines += _threshold_notes()
        return "\n".join(lines) + "\n"


def _single_source(states: dict, label: str) -> str:
    sources = {t.provenance.source for t in states.values()}
    if len(sources) != 1:
        raise ValueError(f"every {label} trace must come from one tool, got {sorted(sources)}")
    return sources.pop()


def _s21_at(trace: RfTrace, freqs: np.ndarray) -> np.ndarray:
    f, s21 = trace.f, trace.s(2, 1)
    return np.array([interp_complex(f, s21, float(q)) for q in freqs], dtype=complex)


def _max_abs(x: np.ndarray) -> float | None:
    x = np.asarray(x, dtype=float)
    finite = x[np.isfinite(x)]
    return float(np.max(np.abs(finite))) if finite.size else None


def compare_states(
    a: dict,
    b: dict,
    reference_state: int = 0,
    f0_hz: float = th.OPERATING_F0_HZ,
    band: Band | None = None,
    n_points: int | None = None,
    comparison: str | None = None,
) -> StateComparison:
    """Compare two tools state by state, keeping only the state dependent difference.

    ``a`` and ``b`` map each commanded state to that tool's trace of the same
    channel in that state. The plain difference ``S21_a,s - S21_b,s`` has a part
    common to every state, which the diagonal array state absorbs and a
    calibration removes. What neither can remove is the state dependent part:

        dphi_s(f) = wrap( wrap(phi_a,s - phi_b,s) - wrap(phi_a,ref - phi_b,ref) )
        dmag_s(f) = (|a_s|dB - |b_s|dB) - (|a_ref|dB - |b_ref|dB)

    judged at every grid point inside the operating band, at both band edges and
    at f0. Phases are subtracted on the circle at both steps. If the tools do
    not both cover the whole operating band the in band verdicts are
    ``unresolved``: nothing is extrapolated to fill the gap.
    """
    if sorted(a) != sorted(b):
        raise ValueError(f"both tools need the same states, got {sorted(a)} and {sorted(b)}")
    if reference_state not in a:
        raise ValueError(f"reference state {reference_state} not among {sorted(a)}")
    if len(a) < 2:
        raise ValueError("need at least one state besides the reference")
    for t in list(a.values()) + list(b.values()):
        if t.n_ports < 2:
            raise ValueError(f"{t.provenance.summary()} has no S21")
    a_src, b_src = _single_source(a, "first"), _single_source(b, "second")
    cls = th.comparison_class([a_src, b_src], comparison)
    band = band or Band(*th.OPERATING_BAND_HZ)

    traces = list(a.values()) + list(b.values())
    shared = common_band(traces)
    covered = shared.start_hz <= band.start_hz and shared.stop_hz >= band.stop_hz
    if covered:
        grid = common_grid(traces, n_points=n_points)
        inside = grid[(grid >= band.start_hz) & (grid <= band.stop_hz)]
        extra = [band.start_hz, band.stop_hz] + ([f0_hz] if band.contains(f0_hz) else [])
        freqs = np.unique(np.concatenate([inside, np.array(extra, dtype=float)]))
    else:
        freqs = np.array([], dtype=float)

    def differential(fq):
        if fq.size == 0:
            return {}
        ref_a, ref_b = _s21_at(a[reference_state], fq), _s21_at(b[reference_state], fq)
        ref_ph = phase_error_deg(np.degrees(np.angle(ref_a)), np.degrees(np.angle(ref_b)))
        ref_mag = mag_db(ref_a) - mag_db(ref_b)
        out = {}
        for s in sorted(a):
            if s == reference_state:
                continue
            va, vb = _s21_at(a[s], fq), _s21_at(b[s], fq)
            ph = phase_error_deg(np.degrees(np.angle(va)), np.degrees(np.angle(vb)))
            out[s] = (
                phase_error_deg(ph, ref_ph),
                (mag_db(va) - mag_db(vb)) - ref_mag,
            )
        return out

    in_band = differential(freqs)
    per_state = {
        s: {"phase_deg_max": _max_abs(p), "mag_db_max": _max_abs(m)}
        for s, (p, m) in in_band.items()
    }
    ph_max = _max_abs(np.concatenate([p for p, _ in in_band.values()])) if in_band else None
    mag_max = _max_abs(np.concatenate([m for _, m in in_band.values()])) if in_band else None

    ph_f0 = mag_f0 = None
    if shared.contains(f0_hz):
        at = differential(np.array([f0_hz]))
        ph_f0 = _max_abs(np.concatenate([p for p, _ in at.values()]))
        mag_f0 = _max_abs(np.concatenate([m for _, m in at.values()]))

    def verdict(key, measured):
        if cls is None:
            return th.UNRESOLVED
        t = th.get(key, cls)
        if t.status != th.NOT_A_LIMIT and t.quantity != th.STATE_DIFFERENTIAL:
            return th.NOT_APPLICABLE
        return t.verdict(measured)

    return StateComparison(
        a_source=a_src,
        b_source=b_src,
        comparison=cls,
        reference_state=reference_state,
        states=sorted(a),
        band=band,
        band_covered=covered,
        f0_hz=f0_hz,
        points_judged=int(freqs.size),
        phase_diff_deg_max=ph_max,
        mag_diff_db_max=mag_max,
        phase_diff_deg_at_f0=ph_f0,
        mag_diff_db_at_f0=mag_f0,
        per_state=per_state,
        verdicts={
            "s21_phase_diff_deg": verdict("s21_phase_diff_deg", ph_max),
            "s21_mag_diff_db": verdict("s21_mag_diff_db", mag_max),
        },
        provenance=[t.provenance.as_dict() for t in traces],
    )
