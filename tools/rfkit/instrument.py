"""Adapter boundary for instrument control. Nothing here talks to an instrument.

The working arrangement for Rev A is deliberately simple:

    analyser  ->  Touchstone file on disk  ->  rfkit

That path needs no driver, no session, and no assumption about which analyser is
on the bench. It also means a measurement is a file with a checksum, which is
what the repository's provenance rule wants.

This module exists so that if automation is wanted later, it arrives behind an
interface instead of being threaded through the analysis code. **Do not import
an instrument library into the analysis modules.** They take Networks and files
and nothing else, which is why they can be tested without hardware.
"""
from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable

from .io import RfTrace, load_touchstone


@runtime_checkable
class SweepSource(Protocol):
    """Anything that can produce a Touchstone file for a requested sweep.

    A file dropped in a directory by hand satisfies this, and so would a driver.
    The analysis code never learns which it was.
    """

    def acquire(self, path: Path) -> Path:
        """Produce a Touchstone file at ``path`` and return the path written."""


class ManualSweep:
    """The Rev A workflow: a human runs the sweep and saves the file.

    This is not a placeholder for a driver. It is the actual first workflow, and
    it is sufficient for every measurement the project currently plans.
    """

    def __init__(self, note: str = "saved from the analyser by hand") -> None:
        self.note = note

    def acquire(self, path: Path) -> Path:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(
                f"{path} does not exist. Save the sweep from the analyser to this "
                "path, then run again. No instrument control is configured, and "
                "that is the intended arrangement for Rev A."
            )
        return path

    def load(self, path: Path, source: str = "vna") -> RfTrace:
        return load_touchstone(self.acquire(path), source=source, note=self.note)


NOTE_ON_AUTOMATION = """
If automation is ever wanted, the shape is:

    class VisaSweep:            # implements SweepSource
        def __init__(self, resource, backend): ...
        def acquire(self, path): ...   # configure, sweep, save Touchstone, return path

and nothing in rfkit.io, rfkit.grid, rfkit.metrics, rfkit.compare, rfkit.state or
rfkit.dataset changes. The instrument library is imported here and nowhere else.

Two things that must not be assumed when that day comes. No native driver for the
analyser observed on this bench has been identified, and the instrument has never
been connected to this computer, so the remote interface is unproven. Both are
recorded in results/EXP-004.
"""
