# 0007. A provisional RF acceptance budget, derived from the quantisation floor

- Status: accepted; every value in it is provisional-theory-derived
- Date: 2026-09-25
- Scope: the verdict thresholds in `tools/rfkit/thresholds.py`, the comparison classes they apply to, and the only ways they may later change

## Question

What limits should `rfkit` apply when it compares two simulators, a simulation with a
measurement, or a design with its requirement, when no simulated or measured
distribution exists yet and no pointing target is recorded anywhere?

## Context

Five verdict metrics existed in `rfkit`, all without a value: S21 magnitude difference,
S21 phase difference, S11 magnitude difference, amplitude imbalance across channels,
and phase spread across channels. The first three were wired to a verdict in the pair
comparison. The last two were computed on the array state and judged by nothing.

**No numeric pointing target exists in this repository.** `docs/architecture/ml-calibration.md`,
EXP-015 in `experiments/plan.md` and decision 0002 all refer to pointing error "below
target", and none gives a value. The benchmark contract asks for curves rather than a
pass mark.

One array level error is fixed by an accepted decision. Decision 0003 chose a three bit
phase shifter, whose rounding leaves a residual that no calibration can remove:

```math
\sigma_q = \frac{45^{\circ}}{\sqrt{12}} = 12.99^{\circ}
```

That floor costs $1.85^{\circ}$ of pointing standard deviation at broadside, $0.167$ dB
of coherent gain and puts the error sidelobe floor at $-18.9$ dB. It is the only
downstream quantity the repository fixes, so it is the anchor.

What the array state absorbs decides what a discrepancy costs.
`docs/mathematics/inverse-calibration.md` section 2 uses the nominal state phases in the
forward model and lets the diagonal state absorb the difference between nominal and
realised. A diagonal state holds one complex number per channel, so it absorbs exactly
the part of an error that does not depend on the commanded state, and the common gain
and phase are unobservable altogether. **The part of any discrepancy common to every
state costs nothing downstream. The state dependent part is not absorbed and reaches the
calibrated beam.** That is why the S21 limits below apply to state differences and not
to the plain difference between two traces.

The unfinished study in `tools/rfkit/budget.py`, resumed here, carried three defects,
all corrected:

| Defect | Correction |
| --- | --- |
| upper band edge offset typed as 1.72 per cent | computed from the band: $+1.78$ per cent, and $-1.64$ at the lower edge |
| gain prediction used the large array limit $e^{-\sigma^{2}}$ | the finite form below; at four elements the limit overstates the loss by a third, 0.223 against 0.167 dB at the floor, and the Monte Carlo agrees with the finite form |
| text stating that thresholds were already set relative to the floor | none were until this record |

## Options considered

### Option A: leave every threshold empty until data exist

Honest, and it inverts the order this repository insists on elsewhere. The first
simulator comparison would receive its data first and an acceptance limit afterwards,
which is the post hoc setting EXP-005 was written to avoid.

### Option B: adopt conventional round tolerances for model agreement

Familiar numbers exist, and none of them is derived from anything this array needs.
There is no evidence here for any of them. Rejected.

### Option C: derive from the quantisation floor, with one declared fraction

Every limit follows from what a discrepancy would do to pointing, coherent gain and
the error sidelobe floor, relative to what the hardware already costs. One policy
number, stated as a policy.

### Option D: derive from a pointing target

The right anchor if it existed. None is recorded and none is planned: the benchmark
reports curves. Waiting for one would leave every comparison without a criterion
indefinitely.

## Comparison

| Criterion | A, empty | B, conventional | C, from the floor | D, from a target |
| --- | --- | --- | --- | --- |
| Limit exists before data | no | yes | yes | no |
| Traceable to this array | not applicable | no | yes | yes, once a target exists |
| Policy inputs | none | every value | one, $\eta$ | the target |
| Main risk | criteria written after the data | false confidence | conservatism of worst case bounds | never starts |

## Evidence

No experimental evidence. The decision rests on decisions 0003 and 0004, the steering
set in `benchmarks/specification.md` section 2, the forward model in
`docs/mathematics/inverse-calibration.md`, and numerical checks in
`tools/rfkit/budget.py` and `tools/rfkit/tests/test_budget.py` under the pinned
environment of `requirements.txt`. The Monte Carlo there confirms the independent error
pointing formula and the finite array gain formula; exact array factor computations
confirm the recorded values at their worst admissible patterns.

## Decision

### The criterion

A discrepancy is acceptable when, in the most damaging arrangement it could take, it adds
at most a fraction $\eta$ of the error variance the quantisation floor already imposes,
on pointing and on coherent gain and sidelobe floor together:

```math
\delta\theta_{\text{worst}}^{2} \le \eta\,\sigma_{\theta,q}^{2},
\qquad
s_{\phi}^{2} + s_{a}^{2} \le \eta\,\sigma_{q}^{2}\left(1 - \frac{1}{N}\right)
```

| Symbol | Meaning | Unit |
| --- | --- | --- |
| $\delta\theta_{\text{worst}}$ | beam shift caused by the discrepancy in its worst pattern | rad |
| $\sigma_{\theta,q}$ | pointing standard deviation caused by quantisation | rad |
| $s_{\phi}^{2}$, $s_{a}^{2}$ | variance across channels, about their mean, of the phase discrepancy and of the relative amplitude discrepancy | rad$^{2}$, dimensionless |
| $\sigma_{q}$ | quantisation residual, 12.99 degrees | rad |
| $N$ | element count, 4 | count |
| $\eta$ | the declared fraction | dimensionless |

**$\eta = 0.10$ is a declared policy, not a measurement.** It says a validation
discrepancy may cost at most a tenth of what the three bit phase shifter already costs:
pointing spread grows by at most 4.9 per cent, and coherent gain loss and the error
sidelobe floor by at most 10 per cent. Every value below scales with $\sqrt{\eta}$, and
`python -m rfkit.cli budget` prints them for 0.05, 0.10 and 0.20 so the consequence of
the choice is visible.

### Sensitivities used, first order, four elements at half wavelength

| Effect | Expression | Consequence |
| --- | --- | --- |
| pointing, per channel error $e_i$ | $\delta\theta = -\dfrac{\sum_i (i-\bar{\imath})\, e_i}{k d \cos\theta_0 \sum_i (i-\bar{\imath})^{2}}$ | only the part linear in element index steers |
| worst pattern bounded by $T$ | $\dfrac{T \sum_i \lvert i-\bar{\imath}\rvert}{k d \cos\theta_0 \sum_i (i-\bar{\imath})^{2}}$ | 1.79 times an independent error of the same rms |
| coherent gain | $G/G_0 \approx 1 - s_{\phi}^{2} - s_{a}^{2}$ | phase in radians and relative amplitude cost gain at the same rate |
| mean gain, independent errors | $e^{-\sigma^{2}} + \left(1 - e^{-\sigma^{2}}\right)/N$ | the finite array form |
| amplitude alone | $\lvert AF \rvert$ is even about the beam for real weights | amplitude does not steer at first order |
| common constant phase | a factor on the whole array factor | costs nothing |
| common proportional error, every state phase scaled by $1+x$ | state dependent, so not common mode | steers; see the design consequence below |

Pointing binds for phase; the amplitude allowance takes what gain and sidelobe budget the
phase bound leaves, so the pair holds jointly.

### Values

| Metric | Class | Value | Applies to | Derivation |
| --- | --- | --- | --- | --- |
| S21 phase difference | two simulators | **2.29 deg** | state dependent part, largest over band 57a and at $f_0$ | $T = \sqrt{\eta}\,\sigma_q \sqrt{5}/4 = 2.296$ |
| S21 magnitude difference | two simulators | **0.40 dB** | as above | $m^{2} = \eta\,\sigma_q^{2}(1-1/N) - T^{2}$, value $20\log_{10}(1+m) = 0.403$ |
| S21 phase difference | simulation against analyser | unresolved | as above, guarded | needs the analyser uncertainty $U$ |
| S21 magnitude difference | simulation against analyser | unresolved | as above, guarded | needs $U$ |
| S11 magnitude difference | both | unresolved | plain difference | no array level consequence in these units, see below |
| amplitude imbalance | design | **0.82 dB** | peak to peak across channels of one array state | $P = 20\log_{10}\dfrac{1+m}{1-m} = 0.826$ |
| channel phase spread | design | not a limit | across channels of one array state | absorbed and corrected, see below |

Values are rounded down to 0.01. The amplitude figures are computed from the recorded
2.29, not from the unrounded bound, so the three recorded values are admissible
together. The exact check at the worst admissible patterns: pointing 0.5831 against a
budget of 0.5848 degrees; gain 0.0161 dB with phase and magnitude together and 0.0166 dB
with phase and imbalance together, against 0.0167 dB. The hard ceiling on any state
error is half a step, 22.5 degrees, beyond which states come out of order.

### Why three comparison classes

| Class | What the difference contains | How it is judged |
| --- | --- | --- |
| design | a property of one array state; no measurement term enters the derivation | directly against the value |
| two simulators, HFSS against ADS | model form, port definitions, and mesh convergence; no measurement | directly against the value. The convergence criterion, the largest change in S between adaptive passes, must be recorded with every solve, and for the verdict to concern models rather than mesh it must satisfy $\Delta S \le \lvert S_{21} \rvert\, T$ with $T$ in radians, about $0.04\,\lvert S_{21} \rvert$ |
| simulation against analyser | the model, the fabrication, and the measurement itself | guarded acceptance: the observed difference plus the analyser's expanded uncertainty must lie within the value. Fabrication is part of what the model has to predict for its downstream use and is judged; the measurement's own error must not be credited to the model. The uncertainty at 2.44 GHz is unknown until EXP-004 O1 names the model and O7 a calibration chain, so both limits stay unresolved |

### The two metrics without a value

**S11 magnitude difference.** Between 50 ohm ports the S21 comparison already carries the
effect of mismatch. What S11 adds is an interaction term with the match of the
neighbouring ports, the divider outputs and the elements, none of which is designed. A
difference in decibels of S11 also has no fixed consequence: ten decibels of disagreement
at $-30$ dB matters less than one at $-6$ dB. The matching requirement itself is a
different question from simulator agreement: a mismatch common to every element is
absorbed by the common gain, and a mismatch that differs between elements appears as
amplitude imbalance, which has its limit above. No separate matching limit is derived.

**Channel phase spread.** A per channel phase offset of any size is absorbed by the
diagonal state and corrected modulo 360 degrees by phase only control, to within the
quantisation floor. This spread is what the calibration exists to remove. A limit on it
would be a performance claim, the experiment's output, rather than an acceptance test.

### In band, and not only at $f_0$

The comparison is judged at every grid point inside band 57a, at both band edges and at
$f_0$, and it refuses to judge a band the traces do not cover. Three reasons: the
downstream criterion holds at every frequency the array may be driven at in the band; a
dispersion discrepancy can vanish at $f_0$ by coincidence; and switched line dispersion
is intrinsic, reaching 5.6 degrees on state 7 at the upper edge. Both tools must
reproduce that term, so their difference is what is judged, not the term.

### A design consequence found on the way, not a threshold

The intrinsic dispersion is a common proportional error, and its array consequence was
computed rather than bounded. At the four benchmark angles, with the worst of the eight
possible command origins, it uses up to 96 per cent of the pointing budget, at 15
degrees. Over a sweep of 0 to 45 degrees in half degree steps, the worst origin exceeds
the budget at 22 of 91 angles, by up to 22 per cent; **choosing the origin per angle keeps
every angle under 49 per cent**. The origin is a free choice, since a common phase is
unobservable. So a steering table that picks it per angle keeps operation anywhere in
band 57a inside the budget, and at $f_0$ the term is zero. This constrains whoever writes
the steering table; no `rfkit` metric enforces it.

The same derivation bounds the hardware's own state dependent phase error against
nominal, which the diagonal state cannot absorb either: 2.29 degrees at $f_0$. No
`rfkit` metric evaluates a tool against the nominal phases yet, so it is recorded here
as a derived design requirement and not wired.

### How later data may, and may not, change these values

Fixed now, before any real HFSS, ADS or analyser data exist:

1. A value changes only through a new decision record, in the same commit as
   `tools/rfkit/thresholds.py`. The tests fail if a recorded value is not its derivation
   rounded down.
2. The permitted triggers are a change of a derivation input: the bit count, element
   count or spacing of decision 0003, the steering set of the benchmark specification,
   $\eta$ by a decision that gives a downstream reason and never a dataset, or a newly
   measured uncertainty term such as the analyser's $U$ or a convergence estimate. Such a
   term is measured by its own procedure, committed before its data and independent of
   the comparisons being judged, for example repeated measurement of one fixed artefact.
3. Forbidden: setting or moving a threshold from the distribution of the very
   discrepancies it judges, and revising after a failure without a trigger from rule 2.
4. If real data show the bound routinely failing on discrepancies whose structure is
   benign, the remedy is a verdict that propagates the discrepancy through the array
   model and judges the resulting pointing and gain against the same budget. The budget
   does not move.
5. Provisional status is lifted by a decision recording both that real distributions
   exist for the comparisons concerned, and that EXP-007, the known cable error, has
   checked the propagation model: the measured beam shift from a known injected phase
   error agrees with the first order prediction within its measurement uncertainty. If
   it does not, the measured coefficient replaces the modelled one by a new decision, and
   the values are recomputed by the derivation, not tuned.

## Consequences

- The switched line network, once it is simulated for layout under gate F5 of
  decision 0006, has acceptance limits for the comparison of its two simulations written
  before their data.
- **The coupling comparison of EXP-011 is not covered.** It compares coupling between
  element ports, which the diagonal model this budget rests on excludes by construction.
  Its acceptance belongs with gate G4, and it has no limit from this record. Decision
  0008 now fixes that test.
- The pair comparison no longer judges plain S21 differences; its verdicts read
  `not applicable` and point to the state by state comparison, `compare_states` in the
  library and `compare-states` on the command line.
- The array state reports its design verdicts.
- Work created: the analyser uncertainty once O1 and O7 are recorded, by a repeatability
  measurement of a fixed artefact; recording $\Delta S$ with every solve; a metric for a
  tool against the nominal state phases; and, if rule 4 is ever triggered, the structure
  aware verdict.
- EXP-015 still has no pointing target. Nothing here is one, and the floor relative
  budget must not be read as one.

## Known limitations

- **Anchored on a floor and a declared fraction, not on a performance target.** If a
  pointing target is ever recorded, these values are re-derived against it.
- **Conservative for proportional discrepancies.** A one per cent common permittivity
  difference between the tools gives 3.15 degrees on state 7 and fails the phase bound,
  while its actual beam shift at the benchmark angles is at most 0.33 degrees, about half
  the budget. The bound covers every pattern because a two tool comparison cannot know
  which pattern a steering table will produce. Rule 4 is the remedy if this bites.
- The floor treats quantisation as independent and uniform across channels. For one
  steering angle the rounding is deterministic; the floor is its average over angles.
- First order sensitivities throughout. They are checked exactly at the recorded values
  for the worst patterns; much larger discrepancies would need the exact propagation.
- The electrical spacing varies by 1.8 per cent across the band, and the coefficients
  with it. Neglected.
- Coupling is excluded: the derivation assumes the diagonal state, as Rev A does, so
  nothing here judges a coupling measurement.

## Conditions for reopening

- Decision 0003 changes the bit count, the element count or the spacing.
- The benchmark steering set changes.
- A numeric pointing target is recorded anywhere in the repository.
- EXP-007 contradicts the propagation model.
- Uncertainty I6 moves the state from diagonal to the full coupling matrix.
- A value is found that the derivation in `tools/rfkit/budget.py` no longer reproduces.
