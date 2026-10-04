#import "../template.typ": *

= Part XI. Validation philosophy <part-xi-validation-philosophy>

```text
   theory                     what must be true in principle              sections 1 to 12
     |
   analytical estimates       what to expect, and how sensitive it is     seeds, budgets, tables
     |
   independent simulation     what the exact geometry gives, two ways     HFSS and a circuit model
     |
   fabrication                the real object, with its coupons           Rev A
     |
   calibrated measurement     what the object does, at known planes       analyser, after O7
     |
   model correction           update material values from coupons         new stack-up revision
     |
   repeated experiment        is it reproducible, across sessions         at least 3 sessions
```

Each level exists because the one above cannot catch a class of error. Theory cannot see a
fabrication tolerance; an analytical model cannot see a discontinuity; a simulation cannot see a
material value it was given wrongly; a single measurement cannot see its own drift; a single
session cannot see what changes between days. The repository's discipline is that a claim may
rest on a level only once the levels below it are satisfied, and that the rule for judging each
level is written before the data reach it.

== 57\. Acceptance budgets

Decision 0007 derived every acceptance threshold from one anchor and one declared policy number,
before any HFSS, ADS or analyser data existed.

*The anchor* is the quantisation floor of section 8: $sigma_q = 12.99$ degrees, costing 1.85
degrees of pointing spread at broadside, 0.167 dB of coherent gain and an error sidelobe floor at
$- 18.9$ dB.

*The policy* is $eta = 0.10$: a validation discrepancy, in its most damaging arrangement, may
add at most a tenth of the error variance the floor already imposes:

$ delta theta_"worst"^2 lt.eq eta thin sigma_(theta , q)^2 , wide s_phi.alt^2 + s_a^2 lt.eq eta thin sigma_q^2 lr(( 1 - frac(1, N) )) $

#table(
  columns: (auto, 4.4fr, 1.8fr),
  table.header([Symbol], [Meaning], [Unit]),
  [$delta theta_"worst"$], [beam shift caused by the discrepancy in its worst pattern], [rad],
  [$sigma_(theta , q)$], [pointing standard deviation caused by quantisation], [rad],
  [$s_phi.alt^2$, $s_a^2$], [variance across channels of the phase discrepancy and of the relative amplitude discrepancy], [rad\$^2\$, dimensionless],
)

$eta = 0.10$ is declared as a policy, not measured: pointing spread may grow by at most 4.9 per
cent, gain loss and the error sidelobe floor by at most 10 per cent. Every value scales with
$sqrt(eta)$, and `python -m rfkit.cli budget` prints them at 0.05, 0.10 and 0.20.

#table(
  columns: (2.8fr, 1.5fr, 1.0fr, 2.5fr, 3.6fr),
  table.header([Metric], [Comparison class], [Value], [Derivation], [Status]),
  [$S_21$ phase difference, state dependent part], [HFSS against ADS], [*2.29 deg*], [$T = sqrt(eta) thin sigma_q sqrt(5) \/ 4 = 2.296$], [provisional-theory-derived],
  [$S_21$ magnitude difference, state dependent part], [HFSS against ADS], [*0.40 dB*], [$m^2 = eta thin sigma_q^2 ( 1 - 1 \/ N ) - T^2$; $20 log_10 ( 1 + m ) = 0.403$], [provisional-theory-derived],
  [amplitude imbalance across channels of one state], [design], [*0.82 dB* peak to peak], [$20 log_10 frac(1 + m, 1 - m) = 0.826$], [provisional-theory-derived],
  [$S_21$ phase and magnitude], [simulation against analyser], [none], [needs the analyser's expanded uncertainty $U$, after O1 and O7], [unresolved],
  [$S_11$ magnitude difference], [both], [none], [no array level consequence in these units], [unresolved],
  [channel phase spread], [design], [not a limit], [it is what calibration removes], [not-a-limit],
  [hardware state dependent phase error against nominal], [design requirement], [2.29 deg at $f_0$], [same derivation; recorded, not wired into a metric], [derived requirement],
)

Three features of the derivation are worth understanding.

- *Only the state dependent part is judged.* A discrepancy common to every state of a channel
  is absorbed by the diagonal array state and costs nothing downstream, so the $S_21$ limits
  apply to state differences, through `compare_states`, not to plain trace differences.
- *The worst pattern, not the typical one.* A comparison of two traces cannot know which
  steering pattern a discrepancy will meet, so the limit bounds the worst arrangement, 1.79 times
  stricter than for an independent error of the same rms. Decision 0007 acknowledges this is
  conservative for proportional discrepancies and names the remedy if it bites: propagate the
  discrepancy through the array model and judge pointing and gain directly, without moving the
  budget.
- *Guarded acceptance against the analyser.* For a simulation against a measurement, the
  observed difference plus the analyser's expanded uncertainty must lie within the limit, so that
  the measurement's own error is never credited to the model. Until $U$ is known at 2.44 GHz,
  those limits stay unresolved.

*Why the thresholds were set before any discrepancy was seen.* A threshold chosen after looking
at a discrepancy can always be chosen to pass it. Decision 0007 therefore also fixed how the values
may change: only by a new decision record, in the same commit as `rfkit.thresholds`, triggered by a
change of a derivation input (bit count, element count, spacing, steering set, $eta$ for a stated
downstream reason, or a newly measured uncertainty term), and never from the distribution of the
discrepancies being judged. The tests fail if a recorded value is not its derivation rounded down.

== 58\. Coupling gate G4

Section 10 explained the physics; this section records the rules of decision 0008 as a validation
procedure.

#table(
  columns: (auto, 10.7fr),
  table.header([Outcome], [Condition, fixed before any data]),
  [*PASS*], [the broadside calibration keeps every judged beam inside the budget, the outcome is the same across the last two mesh passes or across every guard matrix, and the far field route has been checked],
  [*FAIL*], [even the best diagonal leaves a judged beam outside the budget, stably, with the route checked],
  [*INTERMEDIATE*], [anything else: the best diagonal holds but the broadside calibration does not find it; the outcome changes across passes or within the uncertainty; the route is unchecked; the two far field routes disagree],
  [*UNRESOLVED*], [the data do not cover band 57a, the matrix is not passive within tolerance, or a required input is missing],
)

The judged set is every frequency point in band 57a, steering from $- 45$ to $+ 45$ degrees in one
degree steps, all eight command origins, with a calibration over the 29 configurations of the
rotation family at broadside. For measured data, the guard set is the matrix with every coupling
term inflated by $U$ plus 32 reciprocal perturbations of magnitude $U$ from a fixed seed, and the
observed reciprocity defect sets a floor under $U$. Each INTERMEDIATE reason has a named remedy;
a FAIL is promoted in stages, a frozen measured coupling matrix first. A further rule waits on
EXP-005 Phase B: if the calibration residual exceeds the repeatability floor, a pass becomes
intermediate, because the diagonal likelihood is then misspecified at the noise level.

The test is executable, `python -m rfkit.cli g4`, and EXP-011 specifies exactly what each stage
must deliver. No coupling data exist.

== 59\. Stack-up sensitivity

=== 59.1 The derivation

A printed line of length $L$ has phase $phi = beta L$ with
$beta = 2 pi f sqrt(epsilon_"eff") \/ c$. The length is fixed at layout, so an error in
$epsilon_"eff"$ scales every electrical length by the same fraction, exactly:

$ frac(delta phi, phi) = sqrt(1 + frac(delta epsilon_"eff", epsilon_"eff")) - 1 approx frac(1, 2) thin frac(delta epsilon_"eff", epsilon_"eff") $

With the quasi-static model of section 5, $partial epsilon_"eff" \/ partial epsilon_r = ( 1 + F ) \/ 2$,
so to first order

$ delta phi approx frac(theta, 2) dot.op frac(1 + F, 2) dot.op frac(delta epsilon_r, epsilon_"eff") $

#table(
  columns: (auto, 3.5fr, auto),
  table.header([Symbol], [Meaning], [Unit]),
  [$theta$], [designed electrical length: 45, 90, 180, or 315 for state 7], [deg],
  [$F$], [filling factor, about 0.36 on the beamformer construction], [dimensionless],
  [$delta epsilon_r$], [error in the substrate permittivity used at layout], [dimensionless],
)

The chain is: small permittivity error, then a proportional error in $beta$, then a phase error
proportional to line length. *The longest state is the most exposed*: the 180 degree bit carries
four times the error of the 45 degree bit, and state 7, all three bits, seven times. Example from
decision 0009: on the beamformer, an error of 0.2 in $epsilon_r$ moves the 315 degree state by
about 6.5 degrees in this closed form, against the 2.29 degree requirement; `rfkit.stackup`
evaluates the exact line model as well, and the tests hold the two within 10 per cent.

=== 59.2 The tables

#include "../generated/stackup-sensitivity.typ"

What the beamformer's permittivity bound does to the beam, against decision 0007's pointing budget:

#include "../generated/stackup-pointing.typ"

=== 59.3 The 315 degree concern

The error is the same on every channel, so it looks harmless, but it depends on the commanded
state, and decision 0007 showed that such a common proportional error is not absorbed by the
diagonal array state and steers the beam. At 15 degrees of steering the permittivity bound alone
already exceeds the pointing budget, and the worst corner of all bounds roughly doubles it. A
beamformer laid out from a datasheet permittivity would therefore fail decision 0007's derived
requirement before any modelling error is counted. That is why the effective permittivity must be
measured on coupons and the model calibrated to it (section 25), and why the result is an
*analytical concern about a design input, not a measured failure*.

=== 59.4 The loss concern

#include "../generated/stackup-loss.typ"

The 315 degree state's extra loss, 0.59 dB with smooth copper and 0.86 dB with conductor loss
doubled, approaches or exceeds decision 0007's amplitude imbalance allowance of 0.82 dB *for
everything together*, before switch to switch variation, Wilkinson imbalance or connector
differences are counted. Dielectric loss alone is about 0.32 dB of it and does not depend on line
width. Decision 0009 records this as a known limitation with a reopening trigger: if the coupon
attenuation or a simulation of the switched line channel shows the imbalance of one array state
exceeding 0.82 dB, a lower loss laminate is reconsidered. It is deterministic and calculable, so
it does not corrupt the comparison of models with measurements, but it can fail the design check.
*It is an unresolved analytical concern, not a measured failure.*

A further remark, *\[proposed here\]*: because this loss depends on the state, not on the channel,
it is the same for every channel commanded to the same state, and it partly cancels in beams where
the channels occupy similar states. Whether the 0.82 dB allowance, which bounds the spread across
channels of one array state, is actually exceeded depends on the steering table; a propagation of
the state dependent loss through the 512 states would settle it, in the spirit of decision 0007's
rule 4.
