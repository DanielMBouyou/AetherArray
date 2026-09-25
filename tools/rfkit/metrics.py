"""Extraction of the quantities the project actually argues about.

Phase is the part worth reading carefully. Angles live on a circle, so the
difference between 359 degrees and 1 degree is 2 degrees, not 358. Every phase
comparison in this package goes through :func:`wrap_deg`.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np

from .grid import Band, OutOfBand, interp_complex
from .io import RfTrace


def wrap_deg(angle_deg):
    """Wrap an angle, or array of angles, into the half open range [-180, 180).

    The half open convention means exactly +180 maps to -180. That is recorded
    rather than hidden: the two are the same angle, and any consumer comparing
    magnitudes is unaffected.
    """
    return (np.asarray(angle_deg, dtype=float) + 180.0) % 360.0 - 180.0


def phase_error_deg(a_deg, b_deg):
    """Shortest signed angular distance from ``b`` to ``a``, in degrees.

    This is the function that makes 359 against 1 come out as 2 degrees.
    """
    return wrap_deg(np.asarray(a_deg, dtype=float) - np.asarray(b_deg, dtype=float))


def unwrapped_phase_deg(values: np.ndarray) -> np.ndarray:
    """Continuous phase across a sweep, in degrees."""
    return np.degrees(np.unwrap(np.angle(np.asarray(values, dtype=complex))))


def mag_db(values) -> np.ndarray:
    """Magnitude in dB, with zeros mapped to minus infinity rather than a crash."""
    mag = np.abs(np.asarray(values, dtype=complex))
    out = np.full(mag.shape, -np.inf, dtype=float)
    np.log10(mag, out=out, where=mag > 0)
    return 20.0 * out


@dataclass(frozen=True)
class PointMetrics:
    """Everything extracted at a single frequency."""

    f_hz: float
    s11: complex | None
    s21: complex | None
    return_loss_db: float | None
    insertion_loss_db: float | None
    s21_mag_db: float | None
    s21_phase_deg: float | None

    def as_dict(self) -> dict:
        d = asdict(self)
        for key in ("s11", "s21"):
            if d[key] is not None:
                d[key] = {"real": d[key].real, "imag": d[key].imag}
        return d


def extract_at(trace: RfTrace, f0_hz: float) -> PointMetrics:
    """Extract the standard quantities at one frequency.

    Refuses to extrapolate: a frequency outside the trace raises
    :class:`~rfkit.grid.OutOfBand`.
    """
    f = trace.f
    if not (f[0] <= f0_hz <= f[-1]):
        raise OutOfBand(
            f"{f0_hz / 1e9:.6g} GHz lies outside {trace.provenance.summary()} "
            f"[{f[0] / 1e9:.6g}, {f[-1] / 1e9:.6g}] GHz"
        )
    s11 = interp_complex(f, trace.s(1, 1), f0_hz) if trace.n_ports >= 1 else None
    s21 = interp_complex(f, trace.s(2, 1), f0_hz) if trace.n_ports >= 2 else None

    rl = float(-mag_db(np.array([s11]))[0]) if s11 is not None else None
    il = float(-mag_db(np.array([s21]))[0]) if s21 is not None else None
    s21_db = float(mag_db(np.array([s21]))[0]) if s21 is not None else None
    s21_ph = float(wrap_deg(np.degrees(np.angle(s21)))) if s21 is not None else None
    return PointMetrics(
        f_hz=float(f0_hz),
        s11=s11,
        s21=s21,
        return_loss_db=rl,
        insertion_loss_db=il,
        s21_mag_db=s21_db,
        s21_phase_deg=s21_ph,
    )


@dataclass(frozen=True)
class BandMetrics:
    """Summary of a trace over a frequency range."""

    band_start_hz: float
    band_stop_hz: float
    n_points: int
    insertion_loss_db_min: float | None
    insertion_loss_db_max: float | None
    insertion_loss_db_mean: float | None
    return_loss_db_min: float | None
    s21_phase_unwrapped_span_deg: float | None

    def as_dict(self) -> dict:
        return asdict(self)


def extract_band(trace: RfTrace, band: Band | None = None) -> BandMetrics:
    """Summarise a trace over a band, defaulting to its whole sweep."""
    f = trace.f
    lo = band.start_hz if band else float(f[0])
    hi = band.stop_hz if band else float(f[-1])
    mask = (f >= lo) & (f <= hi)
    if not mask.any():
        raise OutOfBand(f"no points of {trace.provenance.summary()} lie in {lo} to {hi} Hz")

    il = rl = None
    span = None
    il_min = il_max = il_mean = rl_min = None
    if trace.n_ports >= 2:
        s21 = trace.s(2, 1)[mask]
        il = -mag_db(s21)
        il_min, il_max, il_mean = float(np.min(il)), float(np.max(il)), float(np.mean(il))
        ph = unwrapped_phase_deg(s21)
        span = float(ph[-1] - ph[0])
    if trace.n_ports >= 1:
        rl = -mag_db(trace.s(1, 1)[mask])
        rl_min = float(np.min(rl))

    return BandMetrics(
        band_start_hz=lo,
        band_stop_hz=hi,
        n_points=int(mask.sum()),
        insertion_loss_db_min=il_min,
        insertion_loss_db_max=il_max,
        insertion_loss_db_mean=il_mean,
        return_loss_db_min=rl_min,
        s21_phase_unwrapped_span_deg=span,
    )


def amplitude_imbalance_db(values) -> float:
    """Spread of channel magnitudes, in dB: the largest minus the smallest.

    ``values`` is a sequence of complex per channel transfers.
    """
    db = mag_db(np.asarray(list(values), dtype=complex))
    if db.size == 0:
        raise ValueError("no channels given")
    return float(np.max(db) - np.min(db))


def phase_spread_deg(values) -> float:
    """Spread of channel phases about their circular mean, in degrees.

    Computed on the circle rather than on raw angles, so a set clustered near
    the wrap point does not report a spurious 360 degree spread.
    """
    v = np.asarray(list(values), dtype=complex)
    if v.size == 0:
        raise ValueError("no channels given")
    mean_angle = np.angle(np.mean(v / np.abs(v)))
    errs = wrap_deg(np.degrees(np.angle(v)) - np.degrees(mean_angle))
    return float(np.max(errs) - np.min(errs))
