"""Analyse a SIM-001 run: protocol steps 7 to 9 of experiments/SIM-001-microstrip-50-ohm.md.

    cd tools
    python sim/sim001_analyse.py --run ../results/SIM-001/raw/run-YYYYMMDD/solve \
        --portcheck ../results/SIM-001/raw/run-YYYYMMDD/portcheck \
        --json ../results/SIM-001/processed/analysis.json

Every number comes from the HFSS exports and their sidecars, read through
``rfkit``. The decision criterion is the one committed before any solve, and it
is applied here as written: convergence first, then the 50 ohm width by linear
interpolation of the port impedance over the three widths, never extrapolated,
then fabricability. What the protocol only asks to report is reported, with no
pass or fail attached.

The dataset is an HFSS physical model. Nothing here is a measurement, and the
labels in the output say so.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
from skrf.io.touchstone import Touchstone

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rfkit import stackup  # noqa: E402
from rfkit.budget import BAND_START_HZ, BAND_STOP_HZ, F0_HZ  # noqa: E402
from rfkit.grid import Band, interp_complex  # noqa: E402
from rfkit.io import load_touchstone  # noqa: E402
from rfkit.lineparams import attenuation_db_per_m, eeff_from_gamma, two_line_gamma  # noqa: E402
from rfkit.metrics import extract_at, extract_band  # noqa: E402
from rfkit.thresholds import THRESHOLDS  # noqa: E402

LABEL = "HFSS physical model, simulation; not a measurement"
BAND_57A = Band(BAND_START_HZ, BAND_STOP_HZ)
PASS, FAIL, UNRESOLVED = "PASS", "FAIL", "UNRESOLVED"


# ----------------------------------------------------------------- criteria, pure
def interpolate_w50(widths_mm, zpi_real_ohm, target_ohm: float = 50.0) -> dict:
    """Criterion 2: the width where the real port impedance equals the target.

    Linear between the two swept widths that bracket the target; never
    extrapolated. Outside the swept range the protocol says recentre and rerun.
    """
    pairs = sorted(zip(widths_mm, zpi_real_ohm))
    for (w1, z1), (w2, z2) in zip(pairs, pairs[1:]):
        if (z1 - target_ohm) * (z2 - target_ohm) <= 0 and z1 != z2:
            w = w1 + (target_ohm - z1) * (w2 - w1) / (z2 - z1)
            return {"w50_mm": w, "bracket_mm": [w1, w2], "verdict": "interpolated"}
    return {"w50_mm": None, "bracket_mm": None,
            "verdict": "outside the swept widths: recentre the sweep and rerun"}


def convergence_verdict(meta: dict, s21_mag: float) -> dict:
    """Criterion 1, and decision 0007's bound on the change in S.

    The final change in S, the pass count and whether HFSS reported convergence
    are copied from the convergence report into the sidecar, protocol step 4.
    Missing values leave the verdict unresolved rather than assumed.
    """
    crit = meta.get("convergence_criterion") or {}
    ds, passes, converged = meta.get("final_delta_s"), meta.get("adaptive_passes"), meta.get("converged")
    if ds is None or passes is None or converged is None:
        return {"verdict": UNRESOLVED, "reason": "convergence not recorded in the sidecar, step 4"}
    t_rad = math.radians(THRESHOLDS[("s21_phase_diff_deg", "hfss_vs_ads")].value)
    bound_0007 = t_rad * s21_mag
    ok = bool(converged) and ds <= crit.get("max_delta_s", float("inf"))
    return {"verdict": PASS if ok else UNRESOLVED,
            "final_delta_s": ds, "adaptive_passes": passes, "converged": bool(converged),
            "decision_0007_bound": bound_0007, "within_0007": ds <= bound_0007,
            "reason": "" if ok else "HFSS did not meet the committed convergence criterion"}


def fabricability_verdict(w50_mm: float | None, st: stackup.Stackup) -> dict:
    """Criterion 3: at least twice the process minimum trace, the narrow flag."""
    if w50_mm is None:
        return {"verdict": UNRESOLVED, "reason": "no 50 ohm width"}
    flags = [f for f in stackup.width_flags(st, "beamformer", w50_mm * 1e-3) if f.startswith("narrow")]
    return {"verdict": FAIL if flags else PASS, "flags": flags}


# ----------------------------------------------------------------- reading the exports
def touchstone_reference(path: Path) -> dict:
    """What a Touchstone file says about its own reference impedance and port data."""
    t = Touchstone(str(path))
    out = {"option_line_ohm": float(np.real(t.resistance)) if t.resistance is not None else None,
           "hfss_port_impedance_comments": bool(getattr(t, "has_hfss_port_impedances", False)),
           "hfss_gamma_comments": t.gamma is not None}
    if out["hfss_port_impedance_comments"]:
        z = np.asarray(t.z0)
        out["comment_z0_first_port_ohm"] = [float(np.real(z[0, 0])), float(np.imag(z[0, 0]))]
    return out


def port_data(path: Path) -> dict:
    """Port impedance and propagation constant written by HFSS, against frequency."""
    t = Touchstone(str(path))
    if t.gamma is None or not getattr(t, "has_hfss_port_impedances", False):
        raise ValueError(f"{path.name} carries no HFSS gamma and port impedance comments")
    f = np.asarray(t.f, dtype=float)
    return {"f": f, "gamma": np.asarray(t.gamma)[:, 0], "zpi": np.asarray(t.z0)[:, 0]}


def _c(z: complex) -> dict:
    return {"real": float(np.real(z)), "imag": float(np.imag(z))}


def load_run(run: Path, st: stackup.Stackup) -> dict:
    designs = {}
    for meta_path in sorted(run.glob("sim001_*.json")):
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        problems = stackup.check_sim_export(meta, st)
        s2p = run / meta["touchstone"]["file"]
        trace = load_touchstone(s2p, source="hfss", note=LABEL, stackup=st.fingerprint)
        designs[meta_path.stem] = {
            "meta": meta, "problems": problems, "trace": trace,
            "reference": touchstone_reference(s2p),
            "port": port_data(run / meta["port_data"]["file"]) if meta.get("port_data") else None,
        }
    if not designs:
        raise FileNotFoundError(f"no SIM-001 sidecars in {run}")
    return designs


# ----------------------------------------------------------------- the analysis
def analyse(run: Path, portcheck: Path | None = None, st: stackup.Stackup | None = None) -> dict:
    st = st or stackup.load()
    designs = load_run(run, st)
    seed = stackup.seed(st, "beamformer")
    per_design, by_width = {}, {}
    for name, d in designs.items():
        v = d["meta"]["variables_mm"]
        pt = extract_at(d["trace"], F0_HZ)
        band = extract_band(d["trace"], BAND_57A)
        zpi = interp_complex(d["port"]["f"], d["port"]["zpi"], F0_HZ) if d["port"] else None
        gport = interp_complex(d["port"]["f"], d["port"]["gamma"], F0_HZ) if d["port"] else None
        per_design[name] = {
            "w_mm": v["w"], "l_mm": v["l"], "label": LABEL, "export_problems": d["problems"],
            "reference": d["reference"],
            "at_f0": {**pt.as_dict(), "s11_mag_db": -pt.return_loss_db},
            "band_57a": band.as_dict(),
            "zpi_at_f0_ohm": _c(zpi) if zpi is not None else None,
            "port_eeff_at_f0": float(eeff_from_gamma(np.array([F0_HZ]), np.array([gport]))[0].real)
            if gport is not None else None,
            "convergence": convergence_verdict(d["meta"], abs(pt.s21)),
        }
        by_width.setdefault(round(v["w"], 6), {})[round(v["l"], 6)] = d
    lines = {}
    for w, pair in sorted(by_width.items()):
        if len(pair) != 2:
            lines[w] = {"verdict": UNRESOLVED, "reason": "both lengths are needed"}
            continue
        (ls, short), (ll, long_) = sorted(pair.items())
        f, g = two_line_gamma(short["trace"], long_["trace"], (ll - ls) * 1e-3)
        ee = eeff_from_gamma(f, g).real
        al = attenuation_db_per_m(g)
        inband = (f >= BAND_57A.start_hz) & (f <= BAND_57A.stop_hz)
        k0 = int(np.argmin(np.abs(f - F0_HZ)))
        zs = [per_design[n]["zpi_at_f0_ohm"]["real"] for n, dd in designs.items()
              if round(dd["meta"]["variables_mm"]["w"], 6) == w and per_design[n]["zpi_at_f0_ohm"]]
        lines[w] = {
            "eeff_at_f0": float(ee[k0]), "alpha_db_per_m_at_f0": float(al[k0]),
            "eeff_band_57a": [float(ee[inband].min()), float(ee[inband].max())],
            "alpha_db_per_m_band_57a": [float(al[inband].min()), float(al[inband].max())],
            "zpi_real_at_f0_ohm": float(np.mean(zs)) if zs else None,
            "zpi_spread_between_lengths_ohm": float(np.ptp(zs)) if zs else None,
        }
    ws = [w for w in lines if lines[w].get("zpi_real_at_f0_ohm") is not None]
    w50 = interpolate_w50(ws, [lines[w]["zpi_real_at_f0_ohm"] for w in ws])
    conv = [d["convergence"]["verdict"] for d in per_design.values()]
    c1 = PASS if all(v == PASS for v in conv) else UNRESOLVED
    c3 = fabricability_verdict(w50["w50_mm"], st)
    seed_w = round(seed["w_seed_m"] * 1e3, 4)
    at_seed = lines.get(round(seed_w, 6), {})
    comparison = {
        "w_seed_mm": seed_w,
        "analytical": {"z0_ohm": 50.0, "eeff": seed["eeff"],
                       "alpha_db_per_m": seed["alpha_c_db_per_m"] + seed["alpha_d_db_per_m"]},
        "hfss": {"zpi_real_ohm": at_seed.get("zpi_real_at_f0_ohm"), "eeff": at_seed.get("eeff_at_f0"),
                 "alpha_db_per_m": at_seed.get("alpha_db_per_m_at_f0")},
    }
    if at_seed.get("eeff_at_f0") is not None:
        comparison["eeff_relative_difference"] = at_seed["eeff_at_f0"] / seed["eeff"] - 1
        comparison["phase_315_deg_equivalent"] = stackup.phase_error_deg(
            stackup.LONGEST_STATE_DEG, seed["eeff"], at_seed["eeff_at_f0"])
    if at_seed.get("zpi_real_at_f0_ohm") is not None:
        comparison["zpi_minus_50_ohm"] = at_seed["zpi_real_at_f0_ohm"] - 50.0
    if w50["w50_mm"] is not None:
        comparison["w50_minus_seed_mm"] = w50["w50_mm"] - seed_w
        comparison["w50_relative_to_seed"] = w50["w50_mm"] / seed_w - 1
    result = {
        "task": "SIM-001", "label": LABEL, "stackup": st.fingerprint, "f0_hz": F0_HZ,
        "designs": per_design, "lines": {f"{w:g}": v for w, v in lines.items()},
        "criterion_1_convergence": c1, "criterion_2_w50": w50,
        "criterion_3_fabricability": c3, "seed_against_hfss": comparison,
    }
    if portcheck is not None:
        result["port_size_check"] = port_size_check(portcheck, per_design, st)
    if c1 != PASS or w50["w50_mm"] is None:
        overall = UNRESOLVED
    else:
        overall = c3["verdict"]
    result["sim001"] = overall
    result["w50_status"] = ("simulation-derived candidate, pending coupon and VNA validation"
                            if w50["w50_mm"] is not None else "none")
    return result


def port_size_check(portcheck: Path, base: dict, st: stackup.Stackup) -> dict:
    """Protocol step 6: change in port impedance and effective permittivity at f0."""
    big = load_run(portcheck, st)
    out = {}
    for name, d in big.items():
        ref = name.split("_ps")[0]
        if ref not in base or d["port"] is None or base[ref]["zpi_at_f0_ohm"] is None:
            continue
        zpi = interp_complex(d["port"]["f"], d["port"]["zpi"], F0_HZ)
        g = interp_complex(d["port"]["f"], d["port"]["gamma"], F0_HZ)
        ee = float(eeff_from_gamma(np.array([F0_HZ]), np.array([g]))[0].real)
        out[name] = {"zpi_change_ohm": float(np.real(zpi)) - base[ref]["zpi_at_f0_ohm"]["real"],
                     "eeff_change": ee - base[ref]["port_eeff_at_f0"]}
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--run", type=Path, required=True)
    ap.add_argument("--portcheck", type=Path, default=None)
    ap.add_argument("--json", type=Path, default=None)
    args = ap.parse_args(argv)
    result = analyse(args.run, args.portcheck)
    text = json.dumps(result, indent=2, default=str)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if result["sim001"] == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
