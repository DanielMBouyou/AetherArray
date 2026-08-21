# 0001. Build the simulator before the array

- Status: accepted
- Date: 2026-08-21
- Scope: how the project is run

## Question

Should we build a physical array first, or first build an array simulator with
injected defects?

## Context

On a real array you do not know the real defects. You can measure whether a
calibration improved the result, but not whether it found the right answer. Yet the
project's question is precisely about comparing estimation methods.

On top of that, the physical array depends on purchases, fabrication, and a
measurement environment whose quality is not yet known.

## Options considered

### Option A: hardware first
Build the array, measure it, then develop the methods. Upside: concrete and
motivating. Downside: you cannot validate an estimation method without knowing the
truth, and everything depends on the quality of the measurement environment.

### Option B: simulator first
Develop and compare the methods on a virtual array whose defects are known, then
apply them to the real one. Upside: method correctness becomes checkable. Downside:
nothing physical for a while.

### Option C: in parallel
The simulator advances while the hardware track progresses at its own pace.

## Comparison

| Criterion | A | B | C |
| --- | --- | --- | --- |
| Ability to validate method correctness | none | complete | complete |
| Dependence on purchases and lead times | strong | none | partial |
| Time to first result | long | short | short |
| Risk if the measurement environment is poor | project blocked | no impact on the simulation track | limited |

## Evidence

No experimental evidence. A methodological argument: an estimation method can only
be validated on a case where the truth is known, which rules out the real array.

Update, 2026-08-21: the tool inventory strengthens this. A full wave electromagnetic
simulator is available, so the coupling injected into the simulator can come from a
physical model of the intended geometry rather than from an invented matrix. That
raises the value of the simulation track considerably.

## Decision

Option C, with priority to the simulator. The simulator is built and checked first,
and the hardware track starts with the measurement environment audit, which costs
nothing.

## Consequences

- The project's first result will be a comparison in simulation.
- The simulator has to be checked carefully, since the whole theoretical track rests
  on it.
- The measurement environment is characterised before any component is bought.
- The coupling model should come from electromagnetic simulation rather than from a
  guess, which adds a task but makes the results far more defensible.

## Known limitations

A simulator reproduces what you thought to put in it. Defects that were not
modelled, for instance an unexpected coupling path or an environmental effect, will
not be captured. Simulation conclusions therefore have to be confronted with the
real array, and the gaps analysed rather than explained away afterwards.

## Conditions for reopening

- If the measurement environment turns out to be excellent, the hardware track can
  be accelerated.
- If the simulator becomes a project in its own right, reduce its ambition and move
  to the real array.
