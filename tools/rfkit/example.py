"""One worked example, end to end, on data that is synthetic and says so.

Produces three Touchstone files standing in for the solver, the circuit
simulator and the analyser, compares them, then builds the array state from four
per channel traces.

**Every number this produces is synthetic.** The traces are constructed from a
formula a few lines below. They demonstrate that the pipeline runs; they are not
evidence about any array, and the files are written with ``synthetic`` in their
provenance so they cannot later be mistaken for measurements.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import skrf

from .compare import compare_all
from .io import load_touchstone, synthetic_trace
from .state import state_from_channel_traces

F0 = 2.44e9


def _two_port(f: np.ndarray, loss_db: float, phase_deg: float, s11_db: float = -18.0):
    """A flat, well behaved two port. Deliberately simple and obviously not real."""
    mag = 10 ** (-loss_db / 20.0)
    ph = np.deg2rad(phase_deg)
    # A little frequency slope so interpolation and unwrapping have something to do.
    slope = np.deg2rad(40.0) * (f - f[0]) / (f[-1] - f[0])
    s21 = mag * np.exp(1j * (ph + slope))
    s11 = np.full_like(f, 10 ** (s11_db / 20.0), dtype=complex)
    s = np.zeros((f.size, 2, 2), dtype=complex)
    s[:, 0, 0] = s11
    s[:, 1, 1] = s11
    s[:, 1, 0] = s21
    s[:, 0, 1] = s21
    return s


def _write(trace, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    ntwk: skrf.Network = trace.network
    ntwk.write_touchstone(str(path.with_suffix("")), form="ri")
    return path


def run_example(out_dir: Path) -> dict:
    out_dir = Path(out_dir)
    raw = out_dir / "raw"
    processed = out_dir / "processed"
    raw.mkdir(parents=True, exist_ok=True)
    processed.mkdir(parents=True, exist_ok=True)

    # Three tools, three different sweeps, on purpose: they overlap but do not
    # coincide, which is the case the grid handling exists for.
    f_hfss = np.linspace(2.30e9, 2.60e9, 61)
    f_ads = np.linspace(2.35e9, 2.55e9, 41)
    f_vna = np.linspace(2.40e9, 2.50e9, 201)

    files = {}
    for name, f, loss, phase in (
        ("hfss_channel0", f_hfss, 3.0, 12.0),
        ("ads_channel0", f_ads, 3.2, 14.0),
        ("vna_channel0", f_vna, 3.4, 17.0),
    ):
        tr = synthetic_trace(f, _two_port(f, loss, phase), note="example, not measured")
        files[name] = _write(tr, raw / f"{name}.s2p")

    traces = [
        load_touchstone(files["hfss_channel0"], source="hfss", note="synthetic example"),
        load_touchstone(files["ads_channel0"], source="ads", note="synthetic example"),
        load_touchstone(files["vna_channel0"], source="vna", note="synthetic example"),
    ]
    report = compare_all(traces, f0_hz=F0)
    (processed / "comparison.txt").write_text(report.to_text(), encoding="utf-8")
    (processed / "comparison.json").write_text(
        json.dumps(report.as_dict(), indent=2) + "\n", encoding="utf-8"
    )

    # Four per channel traces, with deliberate gain and phase errors, so the
    # extracted state has something in it.
    channel_files = {}
    errors = ((0.0, 0.0), (0.4, 25.0), (-0.3, -40.0), (0.9, 170.0))
    for n, (dloss, dphase) in enumerate(errors):
        tr = synthetic_trace(
            f_vna, _two_port(f_vna, 3.4 + dloss, 17.0 + dphase),
            note=f"example channel {n}, not measured",
        )
        channel_files[n] = _write(tr, raw / f"vna_channel{n}.s2p")

    channels = {
        n: load_touchstone(p, source="vna", note="synthetic example")
        for n, p in channel_files.items()
    }
    state = state_from_channel_traces(channels, f0_hz=F0, reference=0,
                                      note="synthetic example, not evidence")
    (processed / "array_state.txt").write_text(state.summary() + "\n", encoding="utf-8")
    (processed / "array_state.json").write_text(
        json.dumps(state.as_dict(), indent=2) + "\n", encoding="utf-8"
    )

    print(report.to_text())
    print(state.summary())
    print(f"\nwritten under {out_dir}")
    print("All of it is synthetic. None of it is evidence about any array.")
    return {"report": report, "state": state, "out_dir": out_dir}
