"""Tests of the SIM-001 analysis on a synthetic run directory.

No HFSS data exist yet, so the run is built analytically: each design is a line
of known characteristic impedance and propagation constant. The renormalised
files are plain Touchstone; the port data files **emulate** HFSS's gamma and
port impedance comments in the layout scikit-rf parses. Once a real HFSS export
exists, a fixture taken from its header replaces the emulation, as the HFSS
dialect regression test.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
import pytest
import skrf
from scipy.constants import c as C0
from skrf.media import DefinedGammaZ0

from rfkit import stackup as su

REPO = Path(__file__).resolve().parents[3]
F = np.linspace(1e9, 3e9, 401)
EEFF = 3.25 - 0.04j


def _module():
    spec = importlib.util.spec_from_file_location(
        "sim001_analyse", REPO / "tools" / "sim" / "sim001_analyse.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


A = _module()


def gamma(f):
    return 1j * 2 * np.pi * f / C0 * np.sqrt(EEFF) + 0.6


def z_line(w_mm):
    """A synthetic impedance law, linear in width, 50 ohm at 0.380 mm."""
    return 50.0 - 80.0 * (w_mm - 0.380)


def write_portdata(path: Path, f, g, z):
    """Emulated HFSS port data: the analysis reads only the comment lines.

    The S data rows are a lossless thru, because nothing reads them.
    """
    lines = ["! Emulated HFSS port data, for tests only", "# HZ S RI R 50"]
    for fk, gk in zip(f, g):
        lines.append(f"{fk:.6e} 0 0 1 0 1 0 0 0")
        lines.append(f"! Gamma ! {gk.real:.9e} {gk.imag:.9e} {gk.real:.9e} {gk.imag:.9e}")
        lines.append(f"! Port Impedance {z:.9e} 0 {z:.9e} 0")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_run(tmp: Path, st, converged=True, widths=None) -> Path:
    tmp.mkdir(parents=True, exist_ok=True)
    p = su.sim001_parameters(st)
    v = p["variables_mm"]
    freq = skrf.Frequency.from_f(F, unit="hz")
    for w in widths or p["width_sweep_mm"]:
        z = z_line(w)
        for length in (v["l_short"], v["l_long"]):
            name = f"sim001_w{w:.4f}_l{length:.1f}".replace(".", "p")
            line = DefinedGammaZ0(frequency=freq, z0_port=50.0, z0=z, gamma=gamma(F))
            net = line.line(length * 1e-3, unit="m")
            net.write_touchstone(str(tmp / name), form="ri")
            write_portdata(tmp / f"{name}-portdata.s2p", F, gamma(F), z)
            meta = {k: None for k in su.SIM_EXPORT_FIELDS}
            meta.update(
                task="SIM-001", stackup=st.fingerprint, construction="beamformer",
                port_impedance_ohm=50.0, renormalised=True,
                final_delta_s=0.008 if converged else None, adaptive_passes=7,
                mesh_elements=12000, converged=converged if converged else None,
                convergence_criterion={"max_delta_s": 0.02, "min_converged_passes": 2},
                variables_mm={**v, "w": w, "l": length},
                touchstone={"file": f"{name}.s2p"}, port_data={"file": f"{name}-portdata.s2p"},
            )
            (tmp / f"{name}.json").write_text(json.dumps(meta), encoding="utf-8")
    return tmp


@pytest.fixture(scope="module")
def st():
    return su.load()


def test_criteria_are_the_committed_ones(st, tmp_path):
    r = A.analyse(make_run(tmp_path / "run", st), st=st)
    assert r["label"] == "HFSS physical model, simulation; not a measurement"
    assert r["criterion_1_convergence"] == "PASS"
    assert r["criterion_2_w50"]["verdict"] == "interpolated"
    assert r["criterion_2_w50"]["w50_mm"] == pytest.approx(0.380, abs=1e-9)
    assert r["criterion_3_fabricability"]["verdict"] == "PASS"
    assert r["sim001"] == "PASS"
    assert "candidate" in r["w50_status"]


def test_line_parameters_and_port_data_are_recovered(st, tmp_path):
    r = A.analyse(make_run(tmp_path / "run", st), st=st)
    eeff_true = (-(gamma(np.array([2.44e9])) * C0 / (2 * np.pi * 2.44e9)) ** 2).real[0]
    for line in r["lines"].values():
        assert line["eeff_at_f0"] == pytest.approx(eeff_true, rel=1e-6)
        assert line["zpi_spread_between_lengths_ohm"] == pytest.approx(0.0, abs=1e-9)
    d = next(iter(r["designs"].values()))
    assert d["port_eeff_at_f0"] == pytest.approx(eeff_true, rel=1e-6)
    assert d["reference"]["hfss_port_impedance_comments"] is False
    assert d["at_f0"]["s21"] is not None and d["band_57a"]["n_points"] > 0
    cmp = r["seed_against_hfss"]
    assert cmp["w_seed_mm"] == pytest.approx(0.372)
    assert cmp["w50_minus_seed_mm"] == pytest.approx(0.008, abs=1e-9)


def test_unrecorded_convergence_leaves_sim001_unresolved(st, tmp_path):
    r = A.analyse(make_run(tmp_path / "run", st, converged=False), st=st)
    assert r["criterion_1_convergence"] == "UNRESOLVED"
    assert r["sim001"] == "UNRESOLVED"


def test_w50_is_never_extrapolated():
    out = A.interpolate_w50([0.30, 0.32, 0.34], [60.0, 58.0, 56.0])
    assert out["w50_mm"] is None and "recentre" in out["verdict"]


def test_a_narrow_w50_fails_fabricability(st):
    assert A.fabricability_verdict(0.15, st)["verdict"] == "FAIL"
    assert A.fabricability_verdict(0.37, st)["verdict"] == "PASS"


def test_convergence_is_checked_against_decision_0007():
    meta = {"final_delta_s": 0.02, "adaptive_passes": 9, "converged": True,
            "convergence_criterion": {"max_delta_s": 0.02}}
    v = A.convergence_verdict(meta, 0.98)
    assert v["verdict"] == "PASS" and v["within_0007"] is True
    assert v["decision_0007_bound"] == pytest.approx(np.radians(2.29) * 0.98)
    meta["converged"] = False
    assert A.convergence_verdict(meta, 0.98)["verdict"] == "UNRESOLVED"


def test_port_size_check_reports_changes(st, tmp_path):
    run = make_run(tmp_path / "run", st)
    big = make_run(tmp_path / "big", st, widths=[0.372])
    for p in big.glob("sim001_*"):
        stem = p.name.split(".")[0].replace("-portdata", "")
        p.rename(p.with_name(p.name.replace(stem, stem + "_ps1p5")))
    for j in big.glob("*.json"):
        meta = json.loads(j.read_text(encoding="utf-8"))
        meta["touchstone"]["file"] = meta["touchstone"]["file"].replace(".s2p", "_ps1p5.s2p")
        meta["port_data"]["file"] = meta["port_data"]["file"].replace("-portdata", "_ps1p5-portdata")
        j.write_text(json.dumps(meta), encoding="utf-8")
    r = A.analyse(run, portcheck=big, st=st)
    assert len(r["port_size_check"]) == 2
    for v in r["port_size_check"].values():
        assert v["zpi_change_ohm"] == pytest.approx(0.0, abs=1e-9)
        assert v["eeff_change"] == pytest.approx(0.0, abs=1e-9)
