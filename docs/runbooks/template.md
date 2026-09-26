# SCH-000: Task name, a verb and an object, then the experiment

- ID: SCH-000
- Class: SCHOOL-BENCH or SCHOOL-SOFTWARE
- Status: TEMPLATE
- Experiment: EXP-000
- Decisions: the decision records whose values this procedure uses
- Last reviewed: YYYY-MM-DD

Copy this file to `docs/runbooks/SCH-NNN-short-name.md`, keep every heading, and replace
every line. The build refuses a runbook that drops a heading, changes their order, or
leaves a placeholder in a runbook marked ready. Write for yourself, arriving at the
machine several days from now with no other context.

## Why we are doing it

Two or three sentences: what this visit unblocks, and which decision or gate is waiting
for it.

## The scientific question

The one question the result answers, in the words of the experiment document.

## What must already be true

- [ ] Each prerequisite as a checkbox: a gate closed, a file produced, a part bought.
- [ ] If one is not true, do not go: the task is not ready.

## What you need

| Item | Why it is needed |
| --- | --- |
| Software and version, or instrument and model | what it does in this task |
| Laptop with the repository | where the results are copied |

## Expected duration

Time at the machine, and time for anything that runs unattended.

## Files to bring or open

| File | Where it is |
| --- | --- |
| This runbook | `docs/runbooks/pdf/SCH-000-name.pdf` |

## Files that must exist when you leave

| File | What it contains |
| --- | --- |
| `YYYY-MM-DD_EXP-000_what.ext` | the result, named as in step 9 |

## STOP / DO NOT CONTINUE

Stop, record why, and leave the machine as you found it, if:

- a condition that would make the run meaningless, such as a wrong stack up, an
  unconverged mesh, a missing calibration, wrong ports or a missing reference plane.

## Procedure

### 1. Open the application or instrument

What to open, and how to know it opened correctly.

### 2. Load the project or set up the connection

Which file or which cables, exactly.

### 3. Settings and parameters

| Setting | Value | Source |
| --- | --- | --- |
| A setting | {{TBD: a value not yet decided; source: the decision that will fix it}} | decision NNNN |

> [!NOTE]
> Why the most important setting has the value it has, in two or three sentences.

### 4. What not to change

- Settings that belong to someone else, or that the result depends on.

### 5. Checks before launching

- [ ] Each thing to verify before pressing run.

### 6. Launch

The exact action that starts the run.

### 7. What success looks like

What the screen shows when the run went right, and what an acceptable null result is.

### 8. Export and save

Exactly what to export, in which format.

### 9. File names and destination

| File | Name | Destination in AetherArray |
| --- | --- | --- |
| The result | `YYYY-MM-DD_EXP-000_what.ext` | `results/EXP-000/raw/YYYY-MM-DD/` |

### 10. Final checklist before leaving

- [ ] Files copied to the laptop and checked.
- [ ] The machine restored to the state you found it in.

## Evidence to bring back

- Screenshots, Touchstone files, solver reports, convergence data, calibration evidence
  and metadata, each named as in step 9.

## Back at home

The exact command that consumes the data, and the next repository task.
