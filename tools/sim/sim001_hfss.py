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
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rfkit import stackup  # noqa: E402

AEDT_VERSION = "2025.2"


def plan(st: stackup.Stackup | None = None, port_scale: float = 1.0,
         seed_only: bool = False) -> dict:
    """The complete model description, in millimetres, with no AEDT involved.

    ``port_scale`` and ``seed_only`` serve protocol step 6, the port size check:
    the seed width, both lengths, with the port and the box enlarged by the
    given factor. Every other number is the canonical file's.
    """
    if port_scale <= 0:
        raise ValueError("port_scale must be positive")
    st = st or stackup.load()
    p = stackup.sim001_parameters(st)
    v = p["variables_mm"]
    widths = [v["w_seed"]] if seed_only else p["width_sweep_mm"]
    suffix = "" if port_scale == 1.0 else f"_ps{port_scale:g}".replace(".", "p")
    designs = []
    for w in widths:
        for length in (v["l_short"], v["l_long"]):
            name = f"sim001_w{w:.4f}_l{length:.1f}".replace(".", "p") + suffix
            pw, ph = v["port_w"] * port_scale, v["port_h"] * port_scale
            h, t = v["sub_h"], v["cu_t"]
            designs.append({
                "name": name, "w_mm": w, "l_mm": length, "port_scale": port_scale,
                "port_w_mm": pw, "port_h_mm": ph,
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


def build(out: Path, student: bool, solve: bool, st: stackup.Stackup | None = None,
          port_scale: float = 1.0, seed_only: bool = False, graphical: bool = False) -> list:
    """Build every planned design into one project, and solve and export if asked.

    Refuses a directory that already holds the project: adding the designs a
    second time would duplicate their geometry. AEDT is released even when a
    step fails, so a failed run leaves no server behind.
    """
    st = st or stackup.load()
    pl = plan(st, port_scale=port_scale, seed_only=seed_only)
    out.mkdir(parents=True, exist_ok=True)
    project = out / "sim001.aedt"
    if project.exists():
        raise FileExistsError(f"{project} exists; build each step into a fresh directory")
    t0 = time.time()
    try:
        return _build(pl, out, str(project), student, solve, st, graphical)
    except BaseException:
        stopped = stop_servers_started_after(t0)
        if stopped:
            print(f"stopped AEDT servers left by this run: {stopped}", file=sys.stderr)
        raise


def stop_servers_started_after(t0: float) -> list:
    """Stop AEDT server processes this run started, after a failure.

    A launch that never connects leaves its server running, and PyAEDT cannot
    release a session it never had. Only processes created after ``t0`` are
    touched, so an AEDT the user opened earlier is left alone.
    """
    try:
        import psutil
    except ImportError:
        return []
    stopped = []
    for proc in psutil.process_iter(["name", "create_time", "pid"]):
        name = (proc.info["name"] or "").lower()
        if name.startswith("ansysedt") and (proc.info["create_time"] or 0) >= t0:
            try:
                proc.kill()
                stopped.append(proc.info["pid"])
            except psutil.Error:
                pass
    return stopped


def _build(pl: dict, out: Path, project: str, student: bool, solve: bool,
           st: stackup.Stackup, graphical: bool) -> list:
    from ansys.aedt.core import Hfss  # imported here so --dry-run needs no AEDT

    p = pl["parameters"]
    m = p["materials"]
    s = p["settings"]
    written = []
    hfss = None
    for d in pl["designs"]:
        hfss = Hfss(project=project, design=d["name"], solution_type="Modal",
                    version=AEDT_VERSION, non_graphical=not graphical, student_version=student)
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
        # The same solution referenced to the ports' own impedance, with HFSS's
        # gamma and port impedance comments: Zpi and the port propagation
        # constant come from here, whatever a renormalised file's comments mean.
        portdata = out / f"{d['name']}-portdata.s2p"
        hfss.export_touchstone(setup="Setup1", sweep="Sweep1", output_file=str(portdata),
                               renormalization=False, gamma_impedance_comments=True)
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
            "mesh_elements": None, "adaptive_passes": None, "final_delta_s": None, "converged": None,
            "convergence_file": conv.name,
            "convergence_criterion": {"max_delta_s": s["max_delta_s"],
                                      "min_converged_passes": s["min_converged_passes"]},
            "boundary": "outer faces perfect electric conductor; ground finite conductivity",
            "materials": m,
            "variables_mm": {**p["variables_mm"], "w": d["w_mm"], "l": d["l_mm"],
                             "port_scale": d["port_scale"], "port_w_used": d["port_w_mm"],
                             "port_h_used": d["port_h_mm"]},
            "touchstone": {"file": s2p.name, "sha256": _sha256(s2p)},
            "port_data": {"file": portdata.name, "sha256": _sha256(portdata),
                          "renormalised": False},
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
    ap.add_argument("--port-scale", type=float, default=1.0,
                    help="enlarge port and box by this factor, protocol step 6")
    ap.add_argument("--seed-only", action="store_true",
                    help="the seed width only, both lengths, protocol step 6")
    ap.add_argument("--graphical", action="store_true",
                    help="show AEDT, for example to see a first launch dialog")
    args = ap.parse_args(argv)
    if args.dry_run:
        print(json.dumps(plan(port_scale=args.port_scale, seed_only=args.seed_only), indent=2))
        return 0
    if args.out is None:
        ap.error("--out is required unless --dry-run")
    for path in build(args.out, args.student, args.solve, port_scale=args.port_scale,
                      seed_only=args.seed_only, graphical=args.graphical):
        print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
