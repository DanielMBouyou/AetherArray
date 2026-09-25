"""Common frequency grid handling.

The rule this module exists to enforce: **traces are only ever compared over
the frequency range they share, and never extrapolated.** A solver sweep, a
circuit simulation and an analyser sweep rarely agree on start, stop or step,
and quietly padding one of them to match another manufactures agreement.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import skrf

from .io import RfTrace


class NoCommonBand(ValueError):
    """Raised when traces share no frequency range at all."""


class OutOfBand(ValueError):
    """Raised when a requested frequency lies outside a trace."""


@dataclass(frozen=True)
class Band:
    start_hz: float
    stop_hz: float

    def contains(self, f_hz: float) -> bool:
        return self.start_hz <= f_hz <= self.stop_hz

    def __str__(self) -> str:
        return f"{self.start_hz / 1e9:.6g} to {self.stop_hz / 1e9:.6g} GHz"


def common_band(traces) -> Band:
    """The frequency range every trace covers.

    Raises :class:`NoCommonBand` rather than returning an empty or inverted
    band, because an empty overlap is a setup error, not a result.
    """
    traces = list(traces)
    if not traces:
        raise NoCommonBand("no traces given")
    start = max(float(t.f[0]) for t in traces)
    stop = min(float(t.f[-1]) for t in traces)
    if not stop > start:
        details = ", ".join(
            f"{t.provenance.summary()} [{t.f[0] / 1e9:.4g}, {t.f[-1] / 1e9:.4g}] GHz"
            for t in traces
        )
        raise NoCommonBand(f"traces share no frequency range: {details}")
    return Band(start, stop)


def common_grid(traces, n_points: int | None = None) -> np.ndarray:
    """Choose the grid on which traces will be compared.

    Default behaviour takes the **coarsest** contributing trace inside the
    shared band, so the comparison never invents resolution that no input had.
    Passing ``n_points`` overrides that with a uniform grid across the band,
    which is the right choice when the inputs are all dense and irregular.
    """
    traces = list(traces)
    band = common_band(traces)
    if n_points is not None:
        if n_points < 2:
            raise ValueError("n_points must be at least 2")
        return np.linspace(band.start_hz, band.stop_hz, int(n_points))

    candidates = []
    for t in traces:
        inside = t.f[(t.f >= band.start_hz) & (t.f <= band.stop_hz)]
        if inside.size >= 2:
            candidates.append(inside)
    if not candidates:
        # Every trace has at most one point inside the overlap. Fall back to the
        # band endpoints rather than guessing a density nobody supplied.
        return np.array([band.start_hz, band.stop_hz], dtype=float)
    return min(candidates, key=lambda a: a.size)


def align(traces, n_points: int | None = None):
    """Interpolate traces onto a shared grid inside their common band.

    Returns ``(aligned_traces, grid)``. Because the grid is built from the
    intersection, no interpolation here is ever an extrapolation.
    """
    traces = list(traces)
    grid = common_grid(traces, n_points=n_points)
    freq = skrf.Frequency.from_f(grid, unit="hz")
    out = []
    for t in traces:
        resampled = t.network.interpolate(freq)
        out.append(t.with_network(resampled, note=f"aligned onto {grid.size} points"))
    return out, grid


def interp_complex(f: np.ndarray, values: np.ndarray, f_query: float) -> complex:
    """Linear interpolation of a complex trace at one frequency.

    Real and imaginary parts are interpolated separately. This is linear
    interpolation and is documented as such: on a sweep dense enough to
    resolve the feature of interest it is adequate, and on one that is not,
    no interpolation scheme would save it.
    """
    f = np.asarray(f, dtype=float)
    values = np.asarray(values, dtype=complex)
    if not (f[0] <= f_query <= f[-1]):
        raise OutOfBand(
            f"{f_query / 1e9:.6g} GHz lies outside "
            f"[{f[0] / 1e9:.6g}, {f[-1] / 1e9:.6g}] GHz; extrapolation is refused"
        )
    re = np.interp(f_query, f, values.real)
    im = np.interp(f_query, f, values.imag)
    return complex(re, im)
