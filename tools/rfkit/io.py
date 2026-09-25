"""Loading Touchstone files into ``skrf.Network`` with provenance attached.

Handles exports from the electromagnetic solver, the circuit simulator and the
network analyser through one path, so that a trace's origin is a field rather
than a filename convention someone has to remember.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import skrf

from .provenance import Provenance

#: Suffixes we accept. ``.sNp`` for any N, as written by all three tools.
TOUCHSTONE_SUFFIX = __import__("re").compile(r"^\.s(\d+)p$", __import__("re").I)


@dataclass(frozen=True)
class RfTrace:
    """One network, plus where it came from.

    The network is never mutated in place. Anything that changes it returns a
    new :class:`RfTrace` carrying forward the provenance.
    """

    network: skrf.Network
    provenance: Provenance

    @property
    def f(self) -> np.ndarray:
        """Frequency points in Hz."""
        return np.asarray(self.network.f, dtype=float)

    @property
    def n_ports(self) -> int:
        return int(self.network.nports)

    def s(self, i: int, j: int) -> np.ndarray:
        """Complex S(i, j) with one-based port numbering, as printed on a plot."""
        return np.asarray(self.network.s[:, i - 1, j - 1])

    def with_network(self, network: skrf.Network, note: str = "") -> "RfTrace":
        prov = Provenance(
            source=self.provenance.source,
            path=self.provenance.path,
            sha256=self.provenance.sha256,
            n_ports=int(network.nports),
            z0_ohm=float(np.real(network.z0[0, 0])),
            f_start_hz=float(network.f[0]),
            f_stop_hz=float(network.f[-1]),
            n_points=len(network.f),
            calibration=self.provenance.calibration,
            note=(self.provenance.note + "; " + note).strip("; "),
        )
        return RfTrace(network=network, provenance=prov)

    def describe(self) -> str:
        p = self.provenance
        return (
            f"{p.source:<9} {self.n_ports}-port  "
            f"{p.f_start_hz / 1e9:.4f} to {p.f_stop_hz / 1e9:.4f} GHz  "
            f"{p.n_points} points  z0={p.z0_ohm:g} ohm  cal={p.calibration}"
        )


def load_touchstone(path: Path | str, source: str, note: str = "") -> RfTrace:
    """Read a Touchstone file of any port count.

    ``source`` is required and not guessed. A trace whose origin is inferred
    from a directory name is a trace whose origin is not recorded.
    """
    path = Path(path)
    if not TOUCHSTONE_SUFFIX.match(path.suffix):
        raise ValueError(
            f"{path.name} does not look like a Touchstone file; expected a .sNp suffix"
        )
    network = skrf.Network(str(path))
    prov = Provenance.from_file(
        path,
        source=source,
        n_ports=int(network.nports),
        z0_ohm=float(np.real(network.z0[0, 0])),
        f_start_hz=float(network.f[0]),
        f_stop_hz=float(network.f[-1]),
        n_points=len(network.f),
        note=note,
    )
    return RfTrace(network=network, provenance=prov)


def load_directory(directory: Path | str, source: str) -> dict[str, RfTrace]:
    """Load every Touchstone file in a directory, keyed by file stem."""
    directory = Path(directory)
    out: dict[str, RfTrace] = {}
    for path in sorted(directory.iterdir()):
        if path.is_file() and TOUCHSTONE_SUFFIX.match(path.suffix):
            out[path.stem] = load_touchstone(path, source=source)
    return out


def synthetic_trace(
    f_hz: np.ndarray,
    s: np.ndarray,
    z0: float = 50.0,
    note: str = "",
) -> RfTrace:
    """Build a trace analytically, marked ``synthetic`` and never anything else.

    ``s`` has shape (points, ports, ports). Used by the tests and the worked
    example. The source field makes it impossible for such a trace to be read
    later as a measurement.
    """
    f_hz = np.asarray(f_hz, dtype=float)
    s = np.asarray(s, dtype=complex)
    if s.ndim != 3 or s.shape[0] != f_hz.size or s.shape[1] != s.shape[2]:
        raise ValueError("s must have shape (points, ports, ports) matching f_hz")
    freq = skrf.Frequency.from_f(f_hz, unit="hz")
    network = skrf.Network(frequency=freq, s=s, z0=z0)
    prov = Provenance(
        source="synthetic",
        n_ports=s.shape[1],
        z0_ohm=float(z0),
        f_start_hz=float(f_hz[0]),
        f_stop_hz=float(f_hz[-1]),
        n_points=int(f_hz.size),
        note=note or "analytically constructed, not a measurement",
    )
    return RfTrace(network=network, provenance=prov)
