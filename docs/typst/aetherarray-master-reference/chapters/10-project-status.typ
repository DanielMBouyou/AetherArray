#import "../template.typ": *

= Part X. Current project status <part-x-current-project-status>

Generated entirely from the repository at the baseline. The status words below map onto the
repository's own: DONE for a recorded, accepted outcome; READY for a task whose prerequisites are
met; IN PROGRESS for partially executed work; BLOCKED for a ready task that failed or waits on an
external prerequisite; NOT STARTED; UNRESOLVED for an open question with no route chosen.

#table(
  columns: (6.0fr, 12.0fr, 16.8fr, 6.9fr, 6.4fr),
  table.header([Area], [Status], [Evidence], [Blocker], [Next action]),
  [project architecture], [DONE], [decisions 0003, 0005, 0009], [none], [none at architecture level],
  [decision records], [DONE, nine accepted], [`decisions/0001` to `0009`], [none], [a decision on the AP-S direction, not yet written],
  [control architecture], [specified, NOT STARTED in hardware], [`docs/architecture/control-architecture.md`], [H1 to H5], [EXP-005 Phase A, part selection],
  [KiCad schematic], [captured, ERC 0 violations, control section superseded], [`hardware/rev-a/README.md`, `erc/erc-report.txt`], [EXP-005 Phase A (R9, H3), H1], [re-capture for decision 0005],
  [stack-up], [DONE], [decision 0009, `reva-stackup-r1:6363d8ab0f2b`], [none], [coupons at layout],
  [HFSS automation], [implemented, dry run tested in CI, never executed successfully], [`tools/sim/sim001_hfss.py`, `results/SIM-001/notes.md`], [AEDT Student opens no scripting session], [open AEDT Student once by hand, rerun step 2],
  [SIM-001], [READY, execution BLOCKED; *no solver data*], [`experiments/SIM-001-microstrip-50-ohm.md`], [as above], [as above],
  [SIM-002 and later], [NOT STARTED; not registered], [only SIM-001 exists], [SIM-001], [register with criteria before data],
  [array simulator, EXP-001], [NOT STARTED], [`experiments/plan.md`, "to do"], [none], [implement; it underpins EXP-002, EXP-012, EXP-013],
  [RF acceptance budget], [DONE, provisional-theory-derived], [decision 0007, `rfkit.thresholds`], [analyser uncertainty for the simulation against analyser class], [EXP-004 O1, O7, then a repeatability measurement],
  [G4 coupling gate], [criterion DONE; no data], [decision 0008, `rfkit.coupling`], [antenna geometry not designed], [SIM-006, then EXP-011 Stage 1],
  [rfkit], [implemented; 160 tests pass on synthetic data], [`tools/rfkit/`, `pytest` at the baseline], [no real data yet], [first real file: SIM-001 output],
  [VNA audit, EXP-004], [IN PROGRESS: 4 complete, 4 partial, 1 not taken], [`results/EXP-004/README.md`], [a bench visit], [run SCH-001 (READY)],
  [EXP-005 Phase A], [READY, NOT STARTED; C1 not run], [`results/EXP-005/README.md`], [B1 to B5 confirmations; harness], [close B1, build harness, run C1],
  [EXP-005 Phase B], [NOT READY], [decision 0006; register SCH-003], [purchases; decision rules not written], [write the rules],
  [purchases], [NOT STARTED; nothing bought], [decision 0006], [O1, O7 for class 2; C1 for the detector], [SCH-001],
  [board fabrication], [NOT STARTED], [decision 0006 gate F1 to F5; F5 half met], [F1 to F5], [clear the gate],
  [antenna design], [NOT STARTED; sanity estimates only], [decision 0009 patch table], [none], [SIM-006],
  [FPGA gateware], [NOT STARTED], [`results/EXP-005/README.md` P2: Quartus 17.1 installed, no programmer ever attached], [none], [EXP-005 harness first],
  [detector], [part selected (AD8318); not bought, not characterised], [decision 0003, V6], [C1 with V1 to V4], [EXP-005 Phase A],
  [ADC], [local converter part not selected; DE1-SoC LTC2308 documented], [decision 0005, H3, T6], [EXP-005 Phase A], [decide H3],
  [machine learning], [formalised; NOT STARTED; no data], [`docs/mathematics/inverse-calibration.md`], [gate G2, which needs the built array], [baselines and simulator first],
  [AP-S proposal], [NOT STARTED; not in the repository], [none], [team, mentor, decision, receiver choice], [read the call in full; decide],
  [scaling study, $N$ up to 128], [NOT STARTED; not in the repository], [none], [EXP-001; measured distributions], [register it if wanted],
  [national frequency allocation check], [NOT STARTED], [decision 0004, conditions for reopening], [none], [a `LOCAL` lookup],
  [PE4259 datasheet reading], [UNRESOLVED], [I18, H1, ERC notes], [the file is a scanned image], [a person reads isolation at 2.44 GHz, thresholds, truth table],
  [licence], [UNRESOLVED], [`LICENSE-NOTES.md`], [none], [a decision before reuse is invited],
)

== 53\. Decision history

#table(
  columns: (52pt, 64pt, 5.6fr, 6.5fr, 7.3fr),
  table.header([Decision, date], [Question], [Decision], [Reason], [Consequence]),
  [0001, 2026-08-21], [hardware first or simulator first?], [simulator and hardware in parallel, simulator first], [a method can only be validated where the truth is known], [the first result is a comparison in simulation; EXP-001 is still to do],
  [0002, 2026-09-17], [where can learning reduce measurements at this scale?], [a learned *drift prior for recalibration*, not a first calibration shortcut], [at $N = 4$ the classical first calibration has little or no count headroom; recalibration has prior information], [the drift experiment becomes central; per element access and temperature telemetry become non retrofittable requirements; gate G2 decides the track],
  [0003, 2026-09-18], [which Rev A RF architecture?], [two boards, four elements, three switched line bits, phase only, per channel enable, detector and analyser paths], [per element access by construction; three bits protect the REV baseline; varactors rejected as a confound], [schematic captured; 29 PE4259-63; amplitude control absent],
  [0004, 2026-09-23], [which working frequency, on what evidence?], [2.44 GHz, band 57a, fixed on direct bench observation], [the only licence exempt band below 3 GHz with no duty cycle limit; an observation is the strongest evidence of coverage], [gate G1 passes; free space quantities fixed; lengths now wait on the stack-up],
  [0005, 2026-09-23], [what drives the array and records the data?], [an external DE1-SoC: FPGA for timing, processor for everything else], [the measurement needs determinism a microcontroller lacks; state correlated error imitates calibration], [registered buffer, local converter as precaution, quiet window; schematic re-capture; Bayesian inverse problem formalised; surrogate pattern synthesis withdrawn],
  [0006, 2026-09-25], [when may hardware be bought?], [staged in four classes, each gated only by what it depends on], [the old rule was circular], [finite pre-fabrication gate F1 to F5; drift half of G2 after fabrication],
  [0007, 2026-09-25], [what acceptance limits, before any data?], [derived from the 3-bit quantisation floor with a declared fraction $eta = 0.10$], [no pointing target exists; limits must precede data], [2.29 degrees, 0.40 dB, 0.82 dB; simulation against analyser unresolved until $U$ is known],
  [0008, 2026-09-26], [how is gate G4 decided?], [a model adequacy test by full propagation on steered beams], [a raw coupling number cannot decide; a calibration residual cannot detect coupling], [executable criterion; staged promotion if it fails],
  [0009, 2026-10-03], [which stack-ups?], [four layer JLC04161H-7628 for the beamformer, two layer 1.6 mm FR-4 for the antennas, calibrated by coupons], [physics of the two boards differs by an order of magnitude; RF laminates cost one to two budgets and still need measuring], [SIM-001 ready; state dependent loss presses on decision 0007's imbalance allowance],
)

Supersessions recorded in the documents: decision 0003's microcontroller by decision 0005; decision
0003's ordering rule by decision 0006; the "no FPGA" answer to uncertainty I10 by decision 0005; the
scheduled surrogate pattern synthesis track of decision 0002's update by decision 0005; the
wording of one sentence of decision 0007 by an erratum in decision 0009.

== 54\. What exists physically today

#table(
  columns: (60pt, 10.3fr, 168pt),
  table.header([Class], [Items], [Evidence]),
  [*owned*], [three Terasic DE1-SoC boards; one Digilent Zybo; two STM32G0 Nucleo boards; three ESP32 boards; a PC], [`docs/hardware/inventory-and-needs.md`; the DE1-SoC count confirmed],
  [*available in the school laboratory, observed*], [a Rohde and Schwarz ZVL vector network analyser, 9 kHz to 3 GHz, two N female ports, complex $S_21$, source to 0 dBm, USB], [*\[observed\]* 2026-09-20, `results/EXP-004/README.md`],
  [*historically documented, presence unconfirmed*], [Agilent N9923A FieldFox, HP 8714C, Agilent N9000A CXA, HP 8562A; 3.5 mm calibration kits belonging to the handheld analyser], [*\[inventory\]*, `docs/hardware/measurement-bench.md` section 2.2],
  [*unconfirmed*], [an oscilloscope, a function generator, any software defined radio, any calibration kit or adapter for the ZVL, a ribbon cable of the intended length, a direct voltage source for EXP-005, a room thermometer, any antenna usable as a probe], [`docs/hardware/inventory-and-needs.md`; EXP-005 section 3],
  [*installed software*], [HFSS Student 2025 R2, Quartus 17.1, KiCad (the generator expects version 10) on the project computer; full HFSS and ADS at school], [SIM-001 notes; EXP-005 P2; `hardware/rev-a/README.md`],
  [*planned, not bought*], [40 PE4259-63, an AD8318, two MCP9808, passives, SMA connectors, jumpers, the two Rev A boards, interconnect, antennas], [decisions 0003 and 0006],
  [*does not exist*], [any Rev A board, fabricated or assembled; any coupon; any antenna board], [this document, Part X],
)

== 55\. What exists in software today

#table(
  columns: (1.8fr, 6.5fr),
  table.header([Item], [State]),
  [`rfkit`], [14 modules, eight command line entry points; 160 tests passing at the baseline on synthetic and analytically constructed data],
  [canonical stack-up], [`reva-stackup-r1`, validated by `rfkit.stackup`, with generated tables in four documents, including this one],
  [SIM-001 builder], [`tools/sim/sim001_hfss.py`, PyAEDT, dry run tested in CI; no successful AEDT execution],
  [SIM-001 analysis], [`tools/sim/sim001_analyse.py` and `rfkit.lineparams`, tested on an emulated run],
  [error budget], [`rfkit.budget`, the derivation of decision 0007, Monte Carlo checked],
  [coupling study], [`rfkit.coupling`, the executable criterion of decision 0008, and a synthetic chart],
  [schematic generator], [`hardware/rev-a/tools/generate-schematic.py`, producing a schematic with four identical channels by construction],
  [runbook system], [`tools/runbooks/build.py`; one runbook, SCH-001, READY, with its PDF],
  [documentation checks], [`tools/check-docs.sh`],
  [figure script for this document], [`tools/docs/master_reference_figures.py`, three analytical figures],
  [not present], [an array simulator (EXP-001), any calibration method implementation (B2 to B6), any gateware, any learning code, any dashboard],
)

== 56\. What has not happened yet

This list exists so that planning maturity is never mistaken for experimental maturity. As of
2026-10-04:

- *No full wave solve has produced a result.* SIM-001's first execution failed before creating
  geometry.
- *No ADS model exists*, and no circuit model of the switched line channel exists in any tool.
- *No board has been fabricated*, assembled or ordered; no part has been bought.
- *No antenna has been designed.*
- *No Rev A characterisation* on the analyser has taken place; no Touchstone file from any
  simulator or instrument has been processed by `rfkit`.
- *No calibrated measurement* has been made with the analyser: no calibration kit is confirmed.
- *EXP-005 has not been run*, not even condition C1.
- *No gateware exists*; no programmer has been attached to the project computer.
- *No drift has been measured*; gate G2 is open and cannot be answered before fabrication.
- *No calibration method has been implemented*, classical or learned; the array simulator of
  EXP-001 does not exist.
- *No learning model exists*, trained or untrained; no dataset exists.
- *No AP-S work exists* in the repository: no decision, no team, no mentor recorded, no receiver
  chosen, no proposal drafted, no sensing or communication experiment designed.
- *No pointing target, null depth target or sensing accuracy target* has been recorded, so
  $M_"required"$ cannot yet be evaluated for any method.
