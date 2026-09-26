# Execution register

- Status: in progress; one school task ready
- Last reviewed: 2026-09-26

Where each current action runs, and the state of every school task. The classes and the
readiness rules are in `README.md`. The check in `tools/runbooks/build.py` reads the
second table, so its columns are fixed.

## 1. Every current action, and where it runs

| Action | Where defined | Class | Why | School task |
| --- | --- | --- | --- | --- |
| Array simulator with injected defects | EXP-001 | `LOCAL` | Python | |
| Calibration methods compared in simulation | EXP-002 | `LOCAL` | Python | |
| Sensitivity to noise and to measurement count | EXP-003 | `LOCAL` | Python | |
| Measurement count bound against the baselines | EXP-012 | `LOCAL` | Python | |
| Learned first calibration estimator, as a control | EXP-013 | `LOCAL` | Python, on the Stage 1 coupling matrix of EXP-011 | |
| Learned drift prior against recalibration | EXP-015 | `LOCAL` | analysis of the EXP-014 dataset | |
| Error budget, state comparison, gate G4 evaluation | decisions 0007 and 0008 | `LOCAL` | `rfkit` | |
| Analyser readings O1 and O6 to O9 | EXP-004 | `SCHOOL-BENCH` | the analyser is in the school laboratory | SCH-001 |
| Acquisition path, Phase A | EXP-005 | `LOCAL` | owned DE1-SoC boards and a direct voltage source | |
| Analyser only reconnection floor | EXP-005 section 9 | `SCHOOL-BENCH` | the analyser | SCH-002 |
| Radio frequency repeatability floor, Phase B | EXP-005 section 9, decision 0006 | `SCHOOL-BENCH` | the analyser is the source and receiver | SCH-003 |
| Coupling of the antenna geometry, Stage 1 | EXP-011 section 3 | `EITHER` | HFSS Student by default; full HFSS only if the converged mesh exceeds 64,000 volume elements | SCH-004, only on escalation |
| Coupling measurement, Stage 2 | EXP-011 section 4 | `SCHOOL-BENCH` | the analyser | SCH-005 |
| Line lengths from the stack up | `hardware/rev-a/layout-constraints.md`, decision 0006 gate F5 | `LOCAL` | closed form and scikit-rf microstrip models | |
| Circuit model of the switched line channel | decision 0007 | `EITHER` | scikit-rf media locally; ADS at school as an optional independent model | SCH-009, optional |
| Full wave model of the beamformer section | decision 0007 | `EITHER` | HFSS Student by default | SCH-010, only on escalation |
| Schematic re-capture for decision 0005, open items H1 to H5 | `hardware/rev-a/README.md` | `LOCAL` | KiCad and data sheets | |
| Switching threshold of the PE4259 on a sample, the fallback for H1 | `docs/architecture/control-architecture.md` section 8 | `EITHER` | a supply and an oscilloscope, whose presence at home is unconfirmed | SCH-011, if at school |
| National table of frequency allocations | decision 0004, conditions for reopening | `LOCAL` | a document lookup | |
| Rev A validation: switched line phases, insertion loss, divider, reflections, per element labels, detector | `docs/hardware/measurement-bench.md` section 4 | `SCHOOL-BENCH` | the analyser | SCH-006 |
| Two element array, known cable error, first calibration, four elements | EXP-006 to EXP-009 | `SCHOOL-BENCH` | the analyser and radiated measurement | SCH-007 |
| Calibration validity over time, unattended rig | EXP-010, EXP-014 | `EITHER` | school if the analyser is the source; local if a dedicated source is bought, decision 0006 class 4 | SCH-008, if at school |

## 2. School tasks

| ID | Task | Class | Status | Runbook | Prerequisite gates | Missing for readiness |
| --- | --- | --- | --- | --- | --- | --- |
| SCH-001 | Finish the network analyser audit, EXP-004 O1 and O6 to O9 | SCHOOL-BENCH | READY | `docs/runbooks/SCH-001-exp004-analyser-audit.md` | none open | nothing |
| SCH-002 | Analyser only reconnection floor, EXP-005 section 9 | SCHOOL-BENCH | NOT READY | none | O7 finds a cable or a through connection | a protocol: repetitions, handling and a decision rule fixed before data; EXP-005 section 9 states only the idea |
| SCH-003 | Radio frequency repeatability floor, EXP-005 Phase B | SCHOOL-BENCH | NOT READY | none | decision 0006: O1 and O7 for interconnect and antennas, C1 with V1 to V4 for the detector | the Phase B decision rules for both routes, written before data; the class 2 purchases themselves |
| SCH-004 | EXP-011 Stage 1 on full HFSS, only if the Student limit is exceeded | SCHOOL-SOFTWARE | NOT READY | none | the antenna geometry exists, and a Student run showed a converged mesh above 64,000 volume elements | the antenna geometry and its HFSS project, a design task not started; the converter from the far field export to the pattern container of EXP-011 section 3 |
| SCH-005 | EXP-011 Stage 2, coupling measurement | SCHOOL-BENCH | NOT READY | none | Rev A fabricated, decision 0006 gate F1 to F5; O1 and O7; matched loads | the analyser uncertainty of EXP-011 section 4.3; the converter to the beamformer container |
| SCH-006 | Rev A validation at the bench | SCHOOL-BENCH | NOT READY | none | Rev A fabricated; the O7 calibration chain; the separate detector, decision 0006 class 2 | a procedure and an acceptance rule for each measurement; `docs/hardware/measurement-bench.md` section 4 lists them only |
| SCH-007 | Radiated experiments, EXP-006 to EXP-009 | SCHOOL-BENCH | NOT READY | none | Rev A; the Phase B floor; antennas | the protocols; the plan details EXP-008 and EXP-009 only once the earlier experiments have run |
| SCH-008 | Long runs, EXP-010 and EXP-014, if run on the school analyser | SCHOOL-BENCH | NOT READY | none | Rev A; the choice of source | whether a dedicated source is bought, which decides whether this is a school task at all; laboratory access for days or weeks, which is not recorded |
| SCH-009 | ADS model of the switched line channel, optional | SCHOOL-SOFTWARE | NOT READY | none | stack up chosen, decision 0006 gate F5 | the stack up and the line lengths; a PE4259 model for ADS with its source identified |
| SCH-010 | Full wave model of the beamformer section on full HFSS, only if the Student limit is exceeded | SCHOOL-SOFTWARE | NOT READY | none | a layout exists | the layout, which is not authorised |
| SCH-011 | PE4259 switching threshold on a sample, if the instruments are only at school | SCHOOL-BENCH | NOT READY | none | the data sheet route for H1 has failed; sample parts bought | whether a supply and an oscilloscope are available at home; the test procedure |
