# 0002. Learning enters as a drift prior, not as a first calibration shortcut

- Status: accepted, with four gates left open and named
- Date: 2026-09-17
- Scope: calibration architecture, the experiment programme, and the capabilities required of the first board

## Question

The project's central research question is whether learned or adaptive methods can
reduce the number of physical measurements needed to reach a target calibrated beam.
In which setting is that question answerable at this project's scale, and what must
the first hardware revision expose for the answer to be measurable rather than
asserted?

## Context

Nothing is built. The element count is expected to be four, the phase shifting route
is expected to be switched line at two bits, and the instrument audit, EXP-004, has
not been done, so it is not yet known whether phase can be measured or only power.

The analysis in `docs/architecture/ml-calibration.md` produced one result that
reorders the whole programme. For an array with $N$ elements and negligible coupling,
the identifiable unknowns number $2N-2$ real parameters, and recovering a complex
vector from intensity measurements alone generically requires at least $4N-4$ real
measurements. At $N = 4$ those are six and twelve. The rotating element field vector
method at its own minimum of three phase states consumes $3N = 12$.

The classical baseline therefore already sits at the information bound. There is no
measurement count left to save on a first calibration at this scale.

## Options considered

### Option A: learned estimator for first calibration

Train a network to recover the channel errors from power measurements, and compare
its measurement count against the rotating element field vector method. This is what
most of the published work does.

Upside: well trodden, and a working result is nearly certain. Downside: at $N = 4$ the
count cannot go below the bound, so any apparent gain would come from comparing
against a padded baseline. It would be a result about the choice of baseline, not
about the method.

### Option B: learned prior across recalibrations

Calibrate fully once, then learn, from the array's own history, how the calibration
drifts with time and temperature, so that later recalibrations start from a prior and
need far fewer measurements.

Upside: the prior removes most of the $2N-2$ dimensions, so the count genuinely falls,
and the claim is attributable to learning. The labels come from running an expensive
classical calibration immediately after the cheap one, on the hardware, so no ground
truth from a model is needed. It is also the setting the literature covers least,
since industrial calibration is a factory operation performed once. Downside: it
depends entirely on drift being measurable, and on the rig being able to run
unattended for weeks.

### Option C: Bayesian optimisation as the learning contribution

Use Bayesian optimisation to search directly for the command giving the best pattern.

Upside: it is the method the repository already names. Downside: it addresses pattern
synthesis, not calibration, and its value is decided by arithmetic rather than by
merit. With $Q$ phase states per channel and one reference channel, exhaustive search
costs $Q^{\,N-1}$ measurements, which is $4^{3} = 64$ at four elements and two bits. A
surrogate cannot produce a result against a brute force baseline of 64 points.

Update, 2026-09-18: decision 0003 selects three bits rather than the two assumed here,
so $Q^{\,N-1}$ becomes $8^{3} = 512$ and the condition in point 3 of the decision below
is met. Bayesian optimisation for pattern synthesis is therefore scheduled. The
decision text needs no change, because it was written as a condition rather than as a
verdict, but the input to that condition has changed and the change is recorded here
rather than left to be rediscovered.

### Option D: decide nothing until the array exists

Build first, choose the algorithmic track afterwards.

Upside: no speculation. Downside: the capabilities that the drift track needs, per
element access above all, cannot be added to a fabricated board. Deciding nothing
decides against option B.

## Comparison

| Criterion | Option A | Option B | Option C | Option D |
| --- | --- | --- | --- | --- |
| Is the measurement count claim defensible at $N = 4$ | no | yes | not applicable | not applicable |
| Labels obtainable on hardware | no, simulation only | yes | none needed | not applicable |
| Data volume required | large | about 100 sessions | none | not applicable |
| Depends on an unanswered gate | no | yes, gate G2 | yes, gate G3 | no |
| Constrains the board | no | yes, and irreversibly | no | forecloses option B |
| Value beyond the literature | low | high | conditional | none |
| Reversibility | high | low once the board is fabricated | high | low |

## Evidence

No experimental evidence, because nothing is built. The decision rests on a counting
argument and on published sources, each checked for author, title, venue and year, and
recorded in `docs/references/bibliography.md`.

- External source: Mano and Katagi, 1982, for the rotating element field vector
  method, and arXiv:2504.16107, 2025, confirming that at least three phase states are
  required and that the count is $KN$.
- External source: Aumann, Fenn and Willwerth, IEEE Transactions on Antennas and
  Propagation, 1989, for the mutual coupling method and for its single stated
  restriction, the ability to transmit and receive with pairs of array elements. That
  restriction is the origin of requirement R1.
- External source: Silverstein, IEEE Transactions on Signal Processing, 1997, for
  orthogonal coding.
- External source: Conca, Edidin, Hering and Vinzant, Applied and Computational
  Harmonic Analysis, 2015, for the $4N-4$ generic injectivity bound. Its applicability
  to the structured rotating element measurement set is marked to verify, not claimed.
- External source: Tambovskiy, Fodor and Tullberg, arXiv:2301.06582, 2023, as the
  precedent for Gaussian process calibration from sparse data.
- Unverified technical opinion, labelled as such: the estimate of about 100 labelled
  recalibration pairs per week of unattended running, which follows from an assumed
  ten minute calibration cycle and has not been measured.

## Decision

Learning enters the project as a **drift prior for recalibration**, option B, and not
as a first calibration shortcut.

Concretely:

1. The central claim to be tested is that a prior learned from the array's own history
   returns pointing error below target using fewer physical measurements than a
   from scratch calibration of the same array needs.
2. A supervised estimator for first calibration is implemented as a **control**, not
   as a contribution, and is compared against the rotating element field vector method
   at its own minimum of three phase states.
3. Bayesian experimental design, the adaptive choice of the next measurement, is the
   method used when the count itself is the target. Bayesian optimisation is reserved
   for pattern synthesis and is run only if $Q^{\,N-1}$ exceeds about 100.
4. Rev A is specified to expose the capabilities listed in
   `docs/hardware/rev-a-requirements.md`, of which per element access and temperature
   telemetry are the two that cannot be retrofitted.
5. The angular positioner is deferred out of the first purchase to pay for those two,
   keeping the total within the budget rule.

## Consequences

- The simulator, decision 0001, is promoted from a checking tool to the training data
  generator, which raises the fidelity requirement on EXP-011's coupling matrix.
- The smallest credible prototype for the ML track is four elements, not two. The two
  element prototype remains valid for the physics demonstration and for EXP-007.
- The drift experiment, EXP-010, moves from an afterthought to the central experiment,
  and the logging schema of requirement R8 has to exist before the first measurement.
- The board topology question, per element connectors against an integrated splitter,
  becomes blocking on the board order.
- `README.md` question 4 and the "learning assisted method, if it adds anything" row
  in its comparison table are both superseded by this decision.
- The bill of materials changes by a swap, not by an increase.

## Known limitations

The decision rests on a counting argument, not on a measurement, and counting
arguments are only as good as their model. If coupling turns out to be significant,
uncertainty I6, the unknowns rise from $2N-2$ to order $2N^{2}$, and the conclusion
that there is no headroom on first calibration has to be recomputed. It may reverse.

The decision also assumes that drift exists at a magnitude worth predicting. That is
not known, and the chosen track dies if it is false. The decision is taken in that
knowledge because the alternative, deferring, forecloses the option irreversibly at
board fabrication.

Nothing here has been validated against a real array, and the estimate of the data
rate an unattended rig can sustain is an estimate.

## Conditions for reopening

- If EXP-005 and EXP-010 show that drift over several hours is smaller than the
  measurement repeatability floor, gate G2 fails: the drift prior track is abandoned,
  and this decision is superseded rather than quietly reinterpreted.
- If EXP-004 finds that phase can be measured directly, the $4N-4$ power only bound
  stops applying, the classical baseline moves to about $2N-2$ complex measurements,
  and the comparison in section 3 of the architecture document is redone.
- If the measured coupling makes the system matrix non diagonal in a way the diagonal
  model cannot absorb, uncertainty I6, reopen the headroom analysis.
- If the element count rises to eight or the phase shifter bit count to three, so that
  $Q^{\,N-1}$ exceeds about 100, the Bayesian optimisation track stops being
  conditional and is scheduled.
- If per element access cannot be afforded within the budget rule, reopen this
  decision before the board is ordered rather than after.
