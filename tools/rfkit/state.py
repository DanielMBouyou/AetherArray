"""From per channel measurements to the array state used by the inverse problem.

The model this serves is in ``docs/mathematics/inverse-calibration.md``. For
Rev A the state is **diagonal**: one complex number per channel. The full
coupling matrix is supported by the data structure so that the extension needs
no rewrite, and it is not the default anywhere.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .grid import interp_complex
from .io import RfTrace
from .metrics import amplitude_imbalance_db, phase_spread_deg, wrap_deg
from .provenance import Provenance

DIAGONAL = "diagonal"
FULL = "full"


@dataclass(frozen=True)
class ArrayState:
    """The complex array state, either diagonal or full.

    ``h`` holds the raw complex values exactly as measured. Relative quantities
    are derived on request rather than stored, so the raw numbers are never
    lost to a gauge choice.
    """

    kind: str
    h: np.ndarray
    f0_hz: float
    reference: int = 0
    provenance: list = field(default_factory=list)
    note: str = ""

    def __post_init__(self) -> None:
        if self.kind not in (DIAGONAL, FULL):
            raise ValueError(f"kind must be {DIAGONAL!r} or {FULL!r}")
        h = np.asarray(self.h, dtype=complex)
        if self.kind == DIAGONAL and h.ndim != 1:
            raise ValueError("a diagonal state is a vector, one entry per channel")
        if self.kind == FULL and (h.ndim != 2 or h.shape[0] != h.shape[1]):
            raise ValueError("a full state is a square matrix")
        if not 0 <= self.reference < self.n_channels:
            raise ValueError("reference channel out of range")

    @property
    def n_channels(self) -> int:
        h = np.asarray(self.h)
        return int(h.shape[0])

    @property
    def diagonal(self) -> np.ndarray:
        """The per channel transfer, for either kind."""
        h = np.asarray(self.h, dtype=complex)
        return h if self.kind == DIAGONAL else np.diagonal(h).copy()

    def as_matrix(self) -> np.ndarray:
        """The state as an N by N matrix, diagonal states being embedded.

        This is the bridge to the coupling extension: code written against the
        matrix form works unchanged when a full state arrives.
        """
        h = np.asarray(self.h, dtype=complex)
        return np.diag(h) if self.kind == DIAGONAL else h.copy()

    def relative(self) -> np.ndarray:
        """Per channel transfer divided by the reference channel.

        A common gain and a common phase are unobservable at the sum port, so
        this is the part that identification can recover: see the count of
        ``2N - 2`` in the inverse calibration document.
        """
        d = self.diagonal
        ref = d[self.reference]
        if ref == 0:
            raise ZeroDivisionError("reference channel has zero transfer")
        return d / ref

    def relative_gain_db(self) -> np.ndarray:
        return 20.0 * np.log10(np.abs(self.relative()))

    def relative_phase_deg(self) -> np.ndarray:
        return wrap_deg(np.degrees(np.angle(self.relative())))

    def identifiable_count(self) -> int:
        """``2N - 2`` for a diagonal state, ``2N^2`` for a full one before gauge."""
        n = self.n_channels
        return 2 * n - 2 if self.kind == DIAGONAL else 2 * n * n

    def amplitude_imbalance_db(self) -> float:
        return amplitude_imbalance_db(self.diagonal)

    def phase_spread_deg(self) -> float:
        return phase_spread_deg(self.diagonal)

    def summary(self) -> str:
        g = self.relative_gain_db()
        p = self.relative_phase_deg()
        rows = [
            f"array state, {self.kind}, {self.n_channels} channels at "
            f"{self.f0_hz / 1e9:.6g} GHz, reference channel {self.reference}",
            f"identifiable real parameters: {self.identifiable_count()}",
            "  ch   relative gain dB   relative phase deg",
        ]
        for n in range(self.n_channels):
            rows.append(f"  {n:<4} {g[n]:>16.4f} {p[n]:>20.3f}")
        rows.append(f"amplitude imbalance: {self.amplitude_imbalance_db():.4f} dB")
        rows.append(f"phase spread       : {self.phase_spread_deg():.3f} deg")
        return "\n".join(rows)

    def as_dict(self) -> dict:
        d = self.diagonal
        return {
            "kind": self.kind,
            "f0_hz": self.f0_hz,
            "reference": self.reference,
            "n_channels": self.n_channels,
            "identifiable_real_parameters": self.identifiable_count(),
            "h_raw": [{"real": v.real, "imag": v.imag} for v in d],
            "relative_gain_db": self.relative_gain_db().tolist(),
            "relative_phase_deg": self.relative_phase_deg().tolist(),
            "amplitude_imbalance_db": self.amplitude_imbalance_db(),
            "phase_spread_deg": self.phase_spread_deg(),
            "provenance": [p.as_dict() for p in self.provenance],
            "note": self.note,
        }


def state_from_channel_traces(
    traces: dict[int, RfTrace],
    f0_hz: float,
    reference: int = 0,
    note: str = "",
) -> ArrayState:
    """Build the Rev A diagonal state from per channel complex S21.

    ``traces`` maps channel index to the measurement of that channel taken
    alone, which on Rev A means one channel enabled and the rest terminated.
    Raw complex values are preserved; nothing is normalised on the way in.
    """
    if not traces:
        raise ValueError("no channel traces given")
    channels = sorted(traces)
    if channels != list(range(len(channels))):
        raise ValueError(f"channels must be 0..N-1 with no gaps, got {channels}")

    h = np.empty(len(channels), dtype=complex)
    prov = []
    for n in channels:
        t = traces[n]
        if t.n_ports < 2:
            raise ValueError(f"channel {n} trace has {t.n_ports} port(s); S21 needs two")
        h[n] = interp_complex(t.f, t.s(2, 1), f0_hz)
        prov.append(t.provenance)
    return ArrayState(
        kind=DIAGONAL, h=h, f0_hz=float(f0_hz), reference=reference,
        provenance=prov, note=note,
    )


def state_from_full_matrix(
    matrix: np.ndarray,
    f0_hz: float,
    reference: int = 0,
    provenance: list | None = None,
    note: str = "",
) -> ArrayState:
    """Build a full coupling state.

    Provided so the data model carries the extension described in the inverse
    calibration document section 2.2. **Rev A does not use this**, and nothing
    in the pipeline selects it by default.
    """
    return ArrayState(
        kind=FULL, h=np.asarray(matrix, dtype=complex), f0_hz=float(f0_hz),
        reference=reference, provenance=list(provenance or []),
        note=note or "full coupling state, an extension beyond the Rev A baseline",
    )
