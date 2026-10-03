"""Build, and optionally solve, the SIM-001 HFSS model from the canonical stack-up.

Every number comes from ``hardware/rev-a/stackup/reva-stackup.json`` through
``rfkit.stackup.sim001_parameters``. This script types none of them, so the
model HFSS solves, the seed scikit-rf computed and the tables in the
documentation all read the same file.

    cd tools
    python sim/sim001_hfss.py --dry-run
    python sim/sim001_hfss.py --out ../results/SIM-001/run-YYYYMMDD --student
    python sim/sim001_hfss.py --out ../results/SIM-001/run-YYYYMMDD --student --solve

The model is a straight microstrip on the beamformer construction: substrate,
trace, air above, a finite conductivity ground, and one wave port at each end.
Outer faces are left as perfect electric conductor, the HFSS default, which
makes it a shielded line; SIM-001 step 6 enlarges the box to check that the
shield does not move the answer. Six designs: three widths times two lengths.

Written against ansys.aedt.core 1.1.0 and AEDT Student 2025 R2. **It had not
been run against AEDT when SIM-001 was declared ready**; running it is step 1 of
``experiments/SIM-001-microstrip-50-ohm.md``.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rfkit import stackup  # noqa: E402

AEDT_VERSION = "2025.2"


def plan(st: stackup.Stackup | None = None) -> dict:
    """The complete model description, in millimetres, with no AEDT involved."""
    st = st or stackup.load()
    p = stackup.sim001_parameters(st)
    v = p["variables_mm"]
    designs = []
    for w in p["width_sweep_mm"]:
        for length in (v["l_short"], v["l_long"]):
            name = f"sim001_w{w:.4f}_l{length:.1f}".replace(".", "p")
            pw, ph, h, t = v["port_w"], v["port_h"], v["sub_h"], v["cu_t"]
            designs.append({
                "name": name, "w_mm": w, "l_mm": length,
                "substrate": {"origin": [-pw / 2, 0.0, 0.0], "sizes": [pw, length, h]},
                "trace": {"origin": [-w / 2, 0.0, h], "sizes": [w, length, t]},
                "air": {"origin": [-pw / 2, 0.0, h], "sizes": [pw, length, ph - h]},
                "ground": {"points": [[-pw / 2, 0.0, 0.0], [pw / 2, 0.0, 0.0],
                                      [pw / 2, length, 0.0], [-pw / 2, length, 0.0]]},
                "ports": [
                    {"name": f"P{i + 1}", "y": y,
                     "points": [[-pw / 2, y, 0.0], [pw / 2, y, 0.0], [pw / 2, y, ph],
                                [-pw / 2, y, ph]],
                     "integration_line": [[0.0, y, 0.0], [0.0, y, h]]}
                    for i, y in enumerate((0.0, length))
                ],
            })
    return {"parameters": p, "designs": designs}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(out: Path, student: bool, solve: bool, st: stackup.Stackup | None = None) -> list:
    from ansys.aedt.core import Hfss  # imported here so --dry-run needs no AEDT

    st = st or stackup.load()
    pl = plan(st)
    p = pl["parameters"]
    m = p["materials"]
    s = p["settings"]
    out.mkdir(parents=True, exist_ok=True)
    project = str(out / "sim001.aedt")
    written = []
    hfss = None
    for d in pl["designs"]:
        hfss = Hfss(project=project, design=d["name"], solution_type="Modal",
                    version=AEDT_VERSION, non_graphical=True, student_version=student)
        hfss.modeler.model_units = "mm"
        sub = hfss.materials.add_material("sim001_substrate")
        sub.permittivity = m["substrate"]["permittivity"]
        sub.dielectric_loss_tangent = m["substrate"]["loss_tangent"]
        cu = hfss.materials.add_material("sim001_copper")
        cu.conductivity = m["copper"]["conductivity_s_per_m"]

        hfss.modeler.create_box(d["substrate"]["origin"], d["substrate"]["sizes"],
                                name="substrate", material="sim001_substrate")
        trace = hfss.modeler.create_box(d["trace"]["origin"], d["trace"]["sizes"],
                                        name="trace", material="sim001_copper")
        air = hfss.modeler.create_box(d["air"]["origin"], d["air"]["sizes"],
                                      name="air", material="vacuum")
        hfss.modeler.subtract(air, [trace], keep_originals=True)
        gnd = hfss.modeler.create_polyline(d["ground"]["points"], close_surface=True,
                                           cover_surface=True, name="ground")
        hfss.assign_finite_conductivity([gnd.name], conductivity=m["copper"]["conductivity_s_per_m"],
                                        name="ground_copper")
        for port in d["ports"]:
            sheet = hfss.modeler.create_polyline(port["points"], close_surface=True,
                                                 cover_surface=True, name=f"{port['name']}_sheet")
            hfss.wave_port(sheet, integration_line=port["integration_line"], modes=1,
                           impedance=s["port_impedance_ohm"], name=port["name"],
                           renormalize=True, characteristic_impedance="Zpi")

        setup = hfss.create_setup("Setup1")
        setup.props["Frequency"] = f"{s['solution_frequency_hz'] / 1e9:g}GHz"
        setup.props["MaximumPasses"] = s["max_passes"]
        setup.props["MaxDeltaS"] = s["max_delta_s"]
        setup.props["MinimumConvergedPasses"] = s["min_converged_passes"]
        setup.update()
        setup.create_linear_step_sweep(unit="GHz", start_frequency=s["sweep_start_hz"] / 1e9,
                                       stop_frequency=s["sweep_stop_hz"] / 1e9,
                                       step_size=s["sweep_step_hz"] / 1e9, name="Sweep1",
                                       sweep_type="Interpolating")
        hfss.save_project()
        if not solve:
            continue
        hfss.analyze_setup("Setup1")
        s2p = out / f"{d['name']}.s2p"
        hfss.export_touchstone(setup="Setup1", sweep="Sweep1", output_file=str(s2p),
                               renormalization=True, impedance=s["port_impedance_ohm"],
                               gamma_impedance_comments=True)
        conv = out / f"{d['name']}-convergence.conv"
        hfss.export_convergence("Setup1", output_file=str(conv))
        meta = {
            "task": "SIM-001", "stackup": st.fingerprint, "construction": p["construction"],
            "solver": "HFSS", "solver_version": AEDT_VERSION,
            "licence": "student" if student else "full",
            "solution_frequency_hz": s["solution_frequency_hz"],
            "sweep": {"start_hz": s["sweep_start_hz"], "stop_hz": s["sweep_stop_hz"],
                      "step_hz": s["sweep_step_hz"], "type": "interpolating"},
            "port_impedance_ohm": s["port_impedance_ohm"],
            "port_definition": "wave port, modal, one mode, Zpi, integration line ground to trace",
            "renormalised": True,
            "mesh_elements": None, "adaptive_passes": None, "final_delta_s": None,
            "convergence_file": conv.name,
            "convergence_criterion": {"max_delta_s": s["max_delta_s"],
                                      "min_converged_passes": s["min_converged_passes"]},
            "boundary": "outer faces perfect electric conductor; ground finite conductivity",
            "materials": m, "variables_mm": {**p["variables_mm"], "w": d["w_mm"], "l": d["l_mm"]},
            "touchstone": {"file": s2p.name, "sha256": _sha256(s2p)},
        }
        (out / f"{d['name']}.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
        written.append(s2p)
    if hfss is not None:
        hfss.release_desktop(close_projects=True, close_desktop=True)
    return written


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true", help="print the model plan, no AEDT")
    ap.add_argument("--out", type=Path, help="directory for the project and the exports")
    ap.add_argument("--student", action="store_true", help="use the AEDT Student licence")
    ap.add_argument("--solve", action="store_true", help="solve and export, not only build")
    args = ap.parse_args(argv)
    if args.dry_run:
        print(json.dumps(plan(), indent=2))
        return 0
    if args.out is None:
        ap.error("--out is required unless --dry-run")
    for path in build(args.out, args.student, args.solve):
        print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
