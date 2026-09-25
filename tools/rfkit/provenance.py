"""Provenance for every RF trace that enters the pipeline.

Nothing in this package accepts a Network without knowing where it came from.
A number whose origin is unrecorded is not evidence, and the repository's own
rule in ``results/README.md`` says as much about measurements.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

#: Recognised origins. ``synthetic`` exists so that analytically constructed
#: traces used in tests and examples can never be mistaken for measurements.
SOURCES = ("hfss", "ads", "vna", "synthetic", "unknown")

#: Calibration state of a trace. Nothing in this package sets anything other
#: than ``none``: no standards, fixtures or corrected measurements exist yet.
CALIBRATION_STATES = ("none", "vendor_applied", "deembedded")


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


@dataclass(frozen=True)
class Provenance:
    """Where a trace came from, and under what conditions."""

    source: str
    path: str | None = None
    sha256: str | None = None
    n_ports: int | None = None
    z0_ohm: float | None = None
    f_start_hz: float | None = None
    f_stop_hz: float | None = None
    n_points: int | None = None
    calibration: str = "none"
    loaded_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds")
    )
    note: str = ""

    def __post_init__(self) -> None:
        if self.source not in SOURCES:
            raise ValueError(f"unknown source {self.source!r}, expected one of {SOURCES}")
        if self.calibration not in CALIBRATION_STATES:
            raise ValueError(f"unknown calibration state {self.calibration!r}")

    @classmethod
    def from_file(cls, path: Path | str, source: str, **kw) -> "Provenance":
        path = Path(path)
        return cls(source=source, path=str(path), sha256=_sha256(path), **kw)

    def as_dict(self) -> dict:
        return asdict(self)

    def summary(self) -> str:
        where = self.path if self.path else "in memory"
        return f"{self.source}:{where}"


def dump_provenance(items, path: Path | str) -> None:
    """Write a provenance record beside a processed output."""
    payload = {
        "written_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "inputs": [p.as_dict() for p in items],
    }
    Path(path).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
