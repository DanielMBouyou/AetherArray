# EXP-011: coupling between the elements, and whether the diagonal state survives it

- Status: planned; the criterion is fixed in decision 0008 and no data exist
- Date: 2026-09-26
- Estimated effort: Stage 1 one solver campaign once the antenna geometry exists; Stage 2 about one day at the bench after fabrication
- Results: `results/EXP-011/`

This experiment settles gate G4. **Its decision rules were fixed before any coupling
was simulated or measured**, in decision 0008 and in `tools/rfkit/coupling.py`, and the
commit introducing this file is the timestamp. A rule may prove unusable, in which case
that is recorded and the experiment is redone; no rule is retuned against a result.

It keeps its first purpose too: the coupling matrix of the real geometry replaces an
invented one in the simulator, which EXP-013 needs whatever G4 concludes.

---

## 1. The question

Does the diagonal array state, calibrated as the bench calibrates it, keep every
steered beam inside the budget once the elements couple? If not, is the failure one of
the calibration or of the model class, and how much of the coupling must enter the
calibration model?

The physical quantities, the forward model and the rules are in decision 0008. This
document says what each stage must deliver so that the rules can be applied.

## 2. The reference plane, and why it matters

The two boards meet at the four element connectors, where the jumpers attach to the
antenna board. **Everything is referred to that plane.** The antenna board is
characterised looking into its connectors. The beamformer is characterised at the far
end of each jumper, so that the jumper belongs to the beamforming side and the two
characterisations cascade at one plane without a gap between them.

Port $n$ is element $n$, counted from one edge, the same numbering as the channels and as
decision 0005's command word. Element 0 is the phase origin of the far field.

## 3. Stage 1, simulation, before fabrication

Runs once the antenna geometry exists. **Nothing here designs it**; spacing and
frequency are fixed by decisions 0003 and 0004.

Where it runs: HFSS Student locally, by default. It moves to the full licence at school,
school task SCH-004, only if the converged mesh, the last two adaptive passes giving
the same verdict, needs more than the Student limit of 64,000 volume elements,
`docs/runbooks/README.md` rule 2.

| Deliverable | Specification |
| --- | --- |
| Antenna board S matrix | four ports at the connector plane, 50 ohm, full $4 \times 4$ matrix, Touchstone real and imaginary format, `.s4p` |
| Frequency grid | 2.30 to 2.60 GHz, uniform, step no coarser than 2.5 MHz, so at least 34 points fall inside band 57a |
| Previous adaptive pass | the same matrix from the pass before the final one, same grid, `.s4p` |
| Embedded element patterns | complex co polar far field in the plane containing the array axis, $\theta$ from $-90$ to $+90$ degrees in steps no coarser than one degree, each port excited alone with the others matched, phase referred to element 0's position, at 2400.0, 2440.0 and 2483.5 MHz |
| Metadata | solver and version, geometry file and its checksum, adaptive pass count, final change in S between passes, solution frequency, boundary conditions, port definitions, substrate constants used |

The patterns are packed into one `.npz` container holding `f_hz` (3), `theta_deg` (G) and
complex `g` of shape (3, 4, G). The conversion from the solver's own export format is
not written yet; the container is what `rfkit` reads.

Command, from `tools/`:

```
python -m rfkit.cli g4 --antenna final.s4p --source hfss \
    --previous-pass previous.s4p --patterns patterns.npz \
    --json ../results/rf/processed/g4-stage1.json --report ../results/rf/processed/g4-stage1.txt
```

Record in `results/EXP-011/` the verdict, its reasons, and **whether the two far field
routes agreed**, which Stage 2 needs.

## 4. Stage 2, measurement, after fabrication

Everything in this stage uses the school analyser: school task SCH-005, whose runbook
cannot be written until Rev A exists and O1 and O7 are recorded.

### 4.1 The antenna board

| Item | Specification |
| --- | --- |
| Instrument | the observed analyser, calibrated at the connector plane through the chain EXP-004 O7 establishes |
| Pairs | all six element pairs, analyser port 1 on the lower index |
| Unused ports | terminated in matched loads whose reflection is measured and recorded |
| Grid | as Stage 1 |
| Settings | IF bandwidth, averaging and source level recorded |
| Environment | the array radiating into the room it will be used in, the room described; then measured again after moving the board by about 0.5 m, so that the difference bounds what the room contributes |
| Assembly | `rfkit.coupling.assemble_from_two_ports`, which averages each reflection over the three pairs that measure it and reports their spread |

### 4.2 The beamforming board

All conducted, at the far end of each jumper.

| Item | Specification | Enters |
| --- | --- | --- |
| Output match | S22 of each channel in each of its 8 states, the common port driven, the other outputs terminated: 32 traces, already taken for the per channel labels | G4 |
| Output isolation | all six output pairs, the common port terminated, the reference state | G4 |
| Forward crosstalk | the transfer of channel $n$ while an adjacent channel cycles through its 8 states | decision 0007, not G4 |

Packed into one `.npz` holding `f_hz`, complex `output_match` of shape (F, 4, 8) and
complex `isolation` of shape (F, 4, 4).

### 4.3 The uncertainty

The expanded uncertainty $U$ of each S term at 2.44 GHz, as a linear magnitude, from the
data sheet of the model EXP-004 O1 identifies, the calibration kit O7 finds, the measured
load reflections, and the environment difference of section 4.1. **It cannot be written
until O1 and O7 are recorded, and until then the measured verdict is unresolved.** The
tool raises it to at least half the reciprocity defect the data show.

Command:

```
python -m rfkit.cli g4 --antenna assembled.s4p --source vna \
    --uncertainty U --beamformer beamformer.npz --stage1-routes-agreed yes \
    --json ../results/rf/processed/g4-stage2.json
```

## 5. Decision rules

Decision 0008, applied as written. In short: **pass** if the broadside calibration keeps
every judged beam inside the budget, stably; **fail** if even the best diagonal cannot,
stably; **intermediate** otherwise, with the evidence each reason requires named in the
decision; **unresolved** if an input is missing or the data are not physical. The judged
set is every frequency point in band 57a with both edges and $f_0$, every steering angle
from $-45$ to $+45$ degrees in one degree steps, and all eight command origins.

A fail promotes the known static coupling model first, and the full matrix only if that
fails too. Decision 0008 lists what each step reopens.

## 6. What this experiment does not decide

- The antenna geometry, the spacing or the frequency.
- Whether the mutual coupling calibration method B6 is viable: that depends on whether
  coupling is measurable above the noise, not on whether it can be neglected, and the
  two questions can have opposite answers.
- The training data of EXP-013, which take the Stage 1 matrix whatever G4 concludes.
- Anything about forward crosstalk, which decision 0007 judges.
