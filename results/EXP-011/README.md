# EXP-011 results

- Status: no data; the criterion was fixed on 2026-09-26, before any
- Last reviewed: 2026-09-26

Protocol in `experiments/EXP-011-coupling-model-adequacy.md`, decision rules in decision
0008. They are applied as written and not adjusted against the data. A cell that was not
obtained stays `to obtain`. **Nothing here is filled from a catalogue, a memory or a
synthetic matrix.**

---

## Stage 1, simulation

### Inputs

| Item | Value |
| --- | --- |
| Solver and version | to obtain |
| Geometry file and checksum | to obtain |
| Final `.s4p` and checksum | to obtain |
| Previous pass `.s4p` and checksum | to obtain |
| Adaptive passes, final change in S | to obtain |
| Embedded patterns container and checksum | to obtain |

### Outcome

| Field | Value |
| --- | --- |
| Verdict | to obtain |
| Reasons, as printed | to obtain |
| Far field routes agree | to obtain, **Stage 2 needs it** |
| Worst broadside calibration, pointing and gain, fraction of budget, and where | to obtain |
| Worst best diagonal, pointing and gain, and where | to obtain |
| Largest coupling, adjacent coupling, row aggregate, in dB | to obtain, descriptive only |
| Screen, and whether it passes | to obtain, descriptive only |
| Recovered state bias, and its change with probe direction | to obtain |

## Stage 2, measurement

### Inputs

| Item | Value |
| --- | --- |
| Analyser model and calibration chain | waits on EXP-004 O1 and O7 |
| Six pair files and checksums | to obtain |
| Load reflections | to obtain |
| Reflection spread across pairs | to obtain |
| Environment difference after moving the board | to obtain |
| Beamformer container and checksum | to obtain |
| Expanded uncertainty $U$, and how it was built | to obtain |

### Outcome

| Field | Value |
| --- | --- |
| Verdict | to obtain |
| Reasons, as printed | to obtain |
| Effective uncertainty after the reciprocity floor | to obtain |
| Guard matrices agreeing with the nominal outcome | to obtain |

## What follows

The consequence of each outcome is fixed in decision 0008, section "What follows from
each outcome". Record here which one applied and what it reopened.
