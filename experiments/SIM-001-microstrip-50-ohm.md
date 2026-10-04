# SIM-001: a 50 ohm microstrip on the Rev A beamformer stack-up

- Status: planned, **READY** since 2026-10-03, see the gate in section 1; **execution blocked
  since 2026-10-03**: AEDT Student starts but opens no scripting session, see
  `results/SIM-001/notes.md`
- Date: 2026-10-03
- Estimated effort: half a day, local
- Actual effort: not run
- Results: `results/SIM-001/`, session notes only; no solver data
- Where: `LOCAL`, HFSS Student; see section 3

## Question

What trace width gives 50 ohm on the beamformer construction of `reva-stackup-r1`, and what
effective permittivity and attenuation does a full wave model give for it at 2.44 GHz and
across band 57a?

The analytical width is only a seed. This simulation decides whether it is acceptable, and
produces the first HFSS Touchstone files to go through `rfkit`.

## 1. Readiness gate

SIM-001 is ready only when all seven hold. Checked on 2026-10-03.

| | Condition | State | Evidence |
| --- | --- | --- | --- |
| 1 | fabrication stack-up selected | met | decision 0009, `reva-stackup-r1` |
| 2 | nominal material model recorded | met | `hardware/rev-a/stackup/reva-stackup.json`, beamformer construction and its materials |
| 3 | uncertainty and tolerance fields exist | met | four reserved bounds per board, enforced by `test_every_construction_reserves_all_four_tolerances` |
| 4 | $W_{\text{seed}}$ computed and explicitly non-final | met | `rfkit.stackup.seed`, labelled INITIALISATION ONLY; table below |
| 5 | HFSS geometry generated from repository parameters | met, with one caveat | `tools/sim/sim001_hfss.py`; `--dry-run` produces the complete geometry from the canonical file and is tested. **The builder had not been executed against AEDT on that date**; step 2 is its first execution, and a failure there is a tooling fault, not a stack-up one |
| 6 | required material values have provenance | met | validator: every value has unit, status and a source present in the bibliography |
| 7 | no unresolved stack-up field prevents a 50 ohm line simulation | met | the open items of decision 0009 are a core permittivity no RF line uses, an order time impedance tolerance, and bounds; none enters the nominal model |

## 2. Inputs, generated

<!-- stackup:begin sim001 -->
Generated from `reva-stackup-r1:6363d8ab0f2b`, construction `beamformer`. **$W_{\text{seed}}$ is not the final width.**

| Variable | Value | Origin |
| --- | --- | --- |
| `sub_h` | 0.2104 mm | PP1 thickness |
| `cu_t` | 0.035 mm | L1 finished copper |
| `w_seed` | 0.372 mm | 50 ohm seed, scikit-rf model |
| `l_short` | 10 mm | fixed choice |
| `l_long` | 27.2 mm | short line plus a quarter guided wavelength at $f_0$ |
| `port_w` | 3.72 mm | the larger of ten widths and the width plus ten heights |
| `port_h` | 2.104 mm | ten substrate heights |
| `sub_er` | 4.4 | PP1 permittivity, nominal |
| `sub_tand` | 0.015 | PP1 loss tangent |
| `cu_sigma` | 5.8e+07 S/m | copper, assumed |
| width sweep | 0.3348, 0.372, 0.4092 mm | the seed scaled by 0.9, 1.0 and 1.1 |

Solution frequency 2.44 GHz; sweep 1 to 3 GHz in 5 MHz steps; maximum change in S 0.02 over 2 consecutive passes, at most 20 passes; ports renormalised to 50 ohm.
<!-- stackup:end sim001 -->

The material values are the stack-up's nominal ones. The permittivity is the fabricator's
calculator value with no stated frequency, and the loss tangent a laminate vendor typical at
1 GHz: SIM-001 measures what the model does with them, not what the board will be. The board
is measured later on its coupons, SCH-012.

## Hypothesis

The seed lies inside the swept widths, so the 50 ohm width is found by interpolation, not by
extrapolation. Nothing more is expected: whether HFSS and the closed form agree is the result,
not a premise.

## Decision criterion

Fixed before any solve.

1. The solve counts only if it converged: largest change in S between adaptive passes at most
   0.02 on two consecutive passes, which satisfies decision 0007's bound of about
   $0.04\,\lvert S_{21} \rvert$ for any line with $\lvert S_{21} \rvert$ above 0.5.
2. $W_{50}$ is the width at which the real part of the HFSS port impedance $Z_{pi}$ equals 50
   ohm at $f_0$, interpolated linearly over the three widths. If it falls outside them, the
   sweep is recentred and rerun; it is never extrapolated.
3. $W_{50}$ is **acceptable** when it is at least twice the process minimum trace of the
   construction, the narrow flag of `rfkit.stackup.width_flags`, so that the published etch
   tolerance does not dominate its impedance. Otherwise the stack-up choice is revisited under
   decision 0009, not the line.
4. Reported, not judged, because no limit exists for them: the difference between $W_{50}$
   and $W_{\text{seed}}$; $\varepsilon_{\text{eff}}$ and attenuation at $f_0$ and over band 57a
   from the two line extraction; their agreement with the port solution's own propagation
   constant; and the change caused by the port size check.

## Setup

- HFSS through AEDT Student 2025 R2, installed locally. Its documented limits are those of 2025
  R1 plus LSDSO not supported, bibliography V23: 64,000 volume elements, four cores, local
  solve.
- `ansys.aedt.core` 1.1.0, and the pinned environment of `requirements.txt` for the analysis.
- Model: substrate, trace, air, a finite conductivity ground and one wave port at each end;
  outer faces perfect electric conductor. Three widths times two lengths, six designs.

## 3. Where it runs

`LOCAL`. The model is a straight line in a box about 4 by 2 by 27 mm, so it is expected to
stay far below the Student mesh limit [assumed]. If a converged mesh ever exceeds 64,000
volume elements, that is first treated as a modelling fault, because a single straight line
should not need it; only if the model is right does it move to the full licence, and only then
does it get a school runbook. Whether the Student edition exports Touchstone with the port
impedance and propagation constant comments is not documented either way, V23; step 5 checks
it.

## Procedure

Raw output goes under `results/SIM-001/raw/run-YYYYMMDD/`, which `results/README.md` keeps out
of git; each step uses a fresh subdirectory, because the builder refuses to add designs to a
project that already has them. Commands are run from `tools/`. Amended on 2026-10-04: the
paths gained the `raw/` level, step 6 gained builder options and steps 7 to 9 a script. No
criterion changed.

1. `python sim/sim001_hfss.py --dry-run`, and check that the fingerprint printed is the one
   `python -m rfkit.cli stackup` prints.
2. Build only: `python sim/sim001_hfss.py --out ../results/SIM-001/raw/run-YYYYMMDD/build-check
   --student`. Open the project, run Validation Check on each design, and look at one design's
   geometry and ports. Add `--graphical` if AEDT has to show itself, for example on a first
   launch.
3. Solve: `--out .../solve --student --solve`. Each design exports a 50 ohm renormalised `.s2p`
   and a `-portdata.s2p` referenced to the ports' own impedance, both with HFSS's gamma and port
   impedance comments.
4. From each convergence file, copy the pass count, the final volume element count, the final
   change in S, and whether HFSS reported the solve converged, into the matching JSON sidecar:
   `adaptive_passes`, `mesh_elements`, `final_delta_s`, `converged`.
5. Check every sidecar with `rfkit.stackup.check_sim_export(meta, rfkit.stackup.load())` and
   that each `.s2p` carries the gamma and impedance comments.
6. Port size check: `--out .../portcheck --student --solve --port-scale 1.5 --seed-only`, the
   seed width, both lengths, port and box enlarged by half.
7. to 9. `python sim/sim001_analyse.py --run .../solve --portcheck .../portcheck --json
   ../results/SIM-001/processed/analysis.json`. It loads every `.s2p` with
   `load_touchstone(path, source="hfss", stackup=fingerprint)`, extracts the propagation
   constant from each pair of lengths by the two line method, `rfkit.lineparams`, reads
   $Z_{pi}$ at $f_0$ from the port data, and applies the decision criterion as written above.
10. Write `results/SIM-001/README.md` with the raw files' checksums, the metadata and the
    verdicts, and record $W_{50}$ in `hardware/rev-a/layout-constraints.md` as a SIM-001
    result.

## What SIM-001 exports

| Item | Form |
| --- | --- |
| S parameters | one `.s2p` per design, renormalised to 50 ohm, with the HFSS gamma and port impedance comments |
| Frequency grid | 1 to 3 GHz in 5 MHz steps, interpolating sweep, adaptive solution at $f_0$ |
| Port reference | wave ports, one mode, $Z_{pi}$, integration line from ground to trace, renormalised to 50 ohm |
| Stack-up | the fingerprint, in every sidecar and in every loaded trace's provenance |
| Mesh and convergence | passes, volume elements, final change in S, the criterion; the exported convergence file |
| Material model | the substrate and copper values the model used, echoed from the canonical file with their status |

`rfkit.stackup.SIM_EXPORT_FIELDS` lists the sidecar fields, and `check_sim_export` refuses a
sidecar that lacks one or names another stack-up. A later VNA measurement of coupon C1 and C2
carries the same fingerprint, so it is traceable to exactly this model.

## Error sources identified before measuring

- The shield: outer faces are perfect conductor; step 6 measures its effect.
- The port: a wave port sized too small couples to the walls; step 6 again.
- Convergence on S rather than on port impedance: the criterion is on S, and the port
  impedance is read from the converged solution.
- Material values with no stated frequency: a limit of the inputs, recorded in decision 0009,
  not of the solve.
- The Student release: the limits were checked for 2025 R2; another release is checked again.

## Independent check

The scikit-rf line model of `rfkit.stackup` gives the seed and its effective permittivity; the
two line extraction and the port solution are two HFSS readings of the same quantity. Three
values, two methods.

## Raw results

None. Not run.

## Analysis

None yet.

## Conclusion

None yet.

## Follow-up

- $W_{50}$ enters `hardware/rev-a/layout-constraints.md` as a simulated value, with its run.
- The same model at 70.7 ohm for the Wilkinson arms, then the switched line channel, decision
  0007's simulator comparison.
- Coupons C1 and C2 at the bench, SCH-012, close the loop between this model and the board.
