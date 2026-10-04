# SIM-001 session notes

- Status: in progress; no solver data yet
- Last reviewed: 2026-10-04

What went wrong during the sessions, in order, per `results/README.md`. Nothing here is a
result: SIM-001 has not produced a solve.

## 2026-10-03, first execution of the builder, protocol step 2

Baseline `main@e772a25082f840d9fabc98e3becc8c40d4a3970a`, clean tree. Stack-up
`reva-stackup-r1:6363d8ab0f2b`; the dry run, step 1, printed the same fingerprint and the
canonical values: substrate 0.2104 mm, permittivity 4.4, loss tangent 0.015, copper
0.035 mm at 5.8e7 S/m, seed width 0.372 mm.

Environment: Windows 11 build 26200.9457; Python 3.12.10; ansys-aedt-core 1.1.0; AEDT
reported as "2025.2SV Student", package R252RC2P01, build 202506171449P01; scikit-rf 1.12.0.
Free memory at launch about 0.7 GB physical and 1.7 GB commit.

Raw output path: `results/SIM-001/raw/run-20261003/`, not the `results/SIM-001/run-YYYYMMDD`
written in the protocol, because `results/README.md` and `.gitignore` keep raw data under
`raw/`. A storage path only; nothing scientific changes.

1. `python sim/sim001_hfss.py --out ../results/SIM-001/raw/run-20261003/build-check --student`.
   AEDT's server process started, about 0.6 GB, but did not open its gRPC port within
   PyAEDT's launch window: launched 21:58:02, failure logged 22:00:56, "Failed to start new
   AEDT gRPC session". Transport WNUA, PyAEDT's secure default. No geometry was created; the
   failure is inside the first `Hfss()` call, before any builder code runs. Log kept as
   `raw/run-20261003/build-check/build.log`.
2. A launch probe with no builder code, `Desktop(non_graphical=True, student_version=True)`
   and the insecure local transport: the same, a server process and no connection.

Both orphaned server processes were stopped. Not attempted a third time.

What the evidence points to, none of it confirmed: `Documents\Ansoft` does not exist, so AEDT
Student has not completed an interactive first launch on this account; a first run, sign-in
or licence dialog cannot be shown in non-graphical mode and would block exactly like this.
`%APPDATA%\Ansys\lastexpdisp.dt` holds `26-Jul-2026`, which looks like the date a licence
expiry notice was last displayed. The licensing client's debug file for this launch is
empty, so licence checkout may never have been reached.

Needed to continue: AEDT Student 2025 R2 opened once by hand, and whatever it shows recorded
here, then step 2 rerun unchanged.

## 2026-10-04, still blocked; tooling completed without AEDT

Nothing in the environment had changed: `Documents\Ansoft` still absent, no AEDT running,
free memory about 0.4 GB physical and 0.75 GB commit. A third launch under the same
conditions was not attempted.

Done instead, all tested without AEDT:

- the builder gained protocol step 6, `--port-scale` and `--seed-only`; `--graphical`, so AEDT
  can show a first launch dialog; a refusal to add designs to an existing project, which
  would duplicate geometry; a second native export per design without renormalisation, so the
  port impedance and propagation constant come from HFSS's own comments; and, on failure, it
  stops the AEDT servers it started, which the failed runs above had left behind;
- `rfkit.lineparams`, the two line extraction of protocol step 8, which coupons C1 and C2
  will reuse;
- `sim/sim001_analyse.py`, steps 7 to 9 with the committed criterion, tested on an emulated
  run. The emulated HFSS comment layout is replaced by a fixture from the first real export.

Still needed: AEDT Student opened once by hand, and memory freed for the solver.
