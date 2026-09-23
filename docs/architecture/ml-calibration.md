# Calibration architecture: where learning belongs, and what it costs the hardware

- Status: in progress, decision recorded in `decisions/0002-learning-as-a-drift-prior.md`
- Last reviewed: 2026-09-17

This document answers one question: can a learned or adaptive method reduce the
number of physical measurements needed to reach a target calibrated beam, and if so,
what must the first hardware revision expose for that claim to be testable.

**The problem it selects is stated formally in `docs/mathematics/inverse-calibration.md`.**
That document gives the forward model, the posterior being inferred, the place where
learned history enters as a prior, and the information gain criterion for choosing the
next measurement. This one decides where learning belongs; that one says what the
problem is.

It is written before any hardware exists, because the answer constrains the board.

---

## 1. The question, sharpened

"Fewer measurements" is not a claim until three things are fixed: fewer than which
baseline, at what accuracy, and in which of two different situations.

| Situation | Definition | Prior information available |
| --- | --- | --- |
| S1, first calibration | the array has never been characterised | none beyond the physical model |
| S2, recalibration | the array was calibrated earlier, and has drifted | the previous calibration, the elapsed time, the temperature history |
| S3, pattern synthesis | find a command giving a target pattern, without estimating the system | none, and the estimate is never formed |

S1 and S2 are calibration. S3 is the neighbouring problem that
`docs/mathematics/formulation.md` section 8 deliberately keeps apart, and it is kept
apart here too. Most published work on learned calibration addresses S1. The analysis
below concludes that S1 is the wrong place to look at this project's scale, and that
S2 is the defensible one.

---

## 2. The non-ML baselines, and what each one costs

A method is characterised by two numbers that trade against each other: how many
physical measurements it consumes, and how much observability the hardware must
provide for it to run at all.

| ID | Method | Source | Measurements | Observability required |
| --- | --- | --- | --- | --- |
| B1 | uncalibrated | control | 0 | none |
| B2 | element by element | classical | $N$ | ability to silence $N-1$ elements; power only yields gains, not phases |
| B3 | rotating element field vector | Mano and Katagi, 1982 | $KN$ with $K \geq 3$ | power only, one fixed probe, commandable phase per element |
| B4 | regularised inversion | classical | $M > N$, set by conditioning rather than by the method | a phase capable receiver, unless a phase retrieval step is put in front |
| B5 | orthogonal coding | Silverstein, 1997 | order $N$ coded measurements | simultaneous coded control of every element |
| B6 | mutual coupling | Aumann, Fenn and Willwerth, 1989 | $N-1$ adjacent pairs at minimum | **transmit and receive on element pairs** |

Numerical example at $N = 4$, the element count this project is most likely to
build:

| Method | Measurements at $N = 4$ | Measurements at $N = 8$ |
| --- | --- | --- |
| B2 | 4 | 8 |
| B3 with $K = 3$ | 12 | 24 |
| B3 with $K = 8$ | 32 | 64 |
| B4 | more than 4, to determine | more than 8, to determine |
| B5 | about 4 | about 8 |
| B6 | 3 | 7 |

Two observations matter more than the numbers themselves.

**The cheap methods are cheap because the hardware gives them more, not because the
algorithm is better.** B6 needs three measurements at $N = 4$, against thirty two for
a comfortable REV. It buys that with a hardware capability, the ability to drive one
element and listen on another, which the project does not currently plan to build.
Measurement count and observability are the same currency.

**B3 is usually quoted with $K$ far above its minimum.** Three phase states determine
a sinusoid, so $K = 3$ is the floor, and the source recorded below confirms that at
least three distinct states are required. Comparing a learned method against REV at
$K = 16$ and calling the difference a contribution would be dishonest. The baseline is
REV at its own minimum.

---

## 3. How much room is actually left on first calibration

This is the part that decides the architecture, and it is settled by counting rather
than by measuring.

If coupling is negligible, the system matrix is diagonal and the unknowns are $N$
complex channel errors:

```math
h_n = g_n\, e^{\,j\psi_n}, \qquad n = 0,\dots,N-1
```

where $g_n$ is the realised amplitude of channel $n$, dimensionless, and $\psi_n$ its
realised phase in radians. That is $2N$ real numbers. A common phase rotation of every
$h_n$, and a common scaling of every $g_n$, leave the sum port reading unchanged, so
neither is identifiable from the array output. The identifiable set is:

```math
d = 2N - 2
```

real parameters, being $N-1$ relative gains and $N-1$ relative phases. At $N = 4$ that
is **six real numbers**. Each scalar power reading yields one real number, so six is
the absolute floor for any method whatsoever, learned or not.

Six is not reachable, because power measurements are not linear in the unknowns.
Recovering a complex vector in $\mathbb{C}^{N}$ from intensity measurements alone, up
to a global phase, generically requires

```math
M \geq 4N - 4
```

real intensity measurements. At $N = 4$ that is **twelve**, which is exactly REV at its
own minimum of $3N = 12$.

The consequence is blunt. **On first calibration, at four elements, with power only
measurement, the classical baseline already sits at the information bound, and there
is no measurement count headroom for a learned method to recover.** A paper reporting a
learned method beating REV on count is, at the scale it was run, either comparing
against a padded $K$, or exploiting structure that is genuine but that disappears when
$N$ is small.

Two caveats, recorded rather than buried. The $4N-4$ result is stated for generic
measurement vectors, and the REV measurement set is highly structured, so the bound is
a guide here and not a theorem about this geometry. That applicability is **[to
verify]**. And the bound concerns injectivity, not accuracy under noise, which is where
the remaining room is.

If coupling is not negligible the count changes completely: a full $\mathbf{H}$ has
$2N^{2}$ real entries, so 32 at $N = 4$, and the argument above has to be redone.
Uncertainty I6 therefore gates this whole section.

---

## 4. Where learning can still contribute

Three settings survive the argument above. They are not equally attractive.

**C1, better estimate at fixed count.** Hold the measurement count at the classical
baseline and improve the estimate under noise. This is what the published learned
methods actually deliver, and the honest restatement of "fewer measurements" is "same
accuracy at lower signal to noise, therefore fewer or shorter integrations". Real,
modest, and already published.

**C2, a learned prior across recalibrations.** After one expensive full calibration,
every later one starts from a prior. If drift is low dimensional, for instance a common
mode phase term driven by temperature plus a slow per channel term, then recalibration
needs far fewer than $4N-4$ measurements, because most of the $2N-2$ dimensions are
already pinned. The prior is learned from the array's own history, and that history
accumulates for free while the array sits on the bench.

This is the only setting in which "fewer physical measurements to reach a target
calibrated beam" is both true and attributable to learning at this scale. It is also
the setting the literature covers least, because industrial calibration is a factory
operation performed once in a chamber, not something repeated for weeks on a bench.

**C3, adaptive choice of the next measurement.** Choose each measurement to maximise
the expected information gain about the parameters, rather than following a fixed
schedule. This is Bayesian experimental design, not Bayesian optimisation: the
objective is posterior entropy about $\mathbf{H}$, not improvement over the best
observed value. The distinction matters, because the repository currently files
Bayesian optimisation under calibration, and that is a category error worth correcting.

Bayesian optimisation proper belongs to S3, and it is gated by arithmetic. With $N$
elements, one reference channel, and $Q$ phase states per channel, exhaustive search
over the command space costs

```math
Q^{\,N-1}
```

measurements. At $N = 4$ with two bit phase shifters, $Q = 4$, that is $4^{3} = 64$
measurements, which a bench can simply run. Any surrogate method has to beat brute
force, and against 64 points it will not beat it by enough to be a result.

**Update, 2026-09-18.** Decision 0003 selects three bits, so $Q = 8$ and the figure for
the array actually being built is $8^{3} = 512$, above the threshold. The track is
therefore scheduled rather than conditional, and the two bit figure above is kept
because it is what makes the threshold legible. At $N = 8$
with three bits the same expression gives $8^{7}$, about 2.1 million, and the surrogate
becomes the only option. **The value of the Bayesian optimisation track is therefore
decided by two hardware numbers, the element count and the phase shifter bit count, and
by nothing else.**

---

## 5. Candidate methods compared

| ID | Method | Measurement cost | Observability required | Data needed | Main failure mode | Scientific value here |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | supervised amortised estimator on power readings | same as B3, no better | as B3 | large simulated set, labels from the simulator only | distribution shift: trained on simulated coupling and error statistics, applied to a real array | low, a reproduction of published work at smaller scale; useful as a control |
| M2 | Gaussian process surrogate of the array response | moderate, sparse sampling of the response | as B3, plus repeatable positioning | tens to hundreds of points, no labels needed | extrapolates poorly outside the sampled region; kernel choice carries the result | medium, and the model class suits the data budget |
| M3 | learned drift prior, recalibration from a previous solution | **the quantity under test**, expected well below $4N-4$ | as B3, plus unattended repeat measurement and temperature logging | one labelled pair per session, order 100 sessions | drift dominated by connector handling rather than by time and temperature, making it unpredictable in principle | **high, and the part the literature does not cover** |
| M4 | Bayesian experimental design, adaptive schedule | targets count directly, bounded below by $4N-4$ | as B3 | none, the model is the physics | little room at $N = 4$; gains grow with $N$ | medium, and it is the honest version of the measurement count claim |
| M5 | Bayesian optimisation for pattern synthesis | many evaluations | as B3 | none | brute force wins when $Q^{N-1}$ is small | conditional, see the arithmetic in section 4 |

M1 is kept because a comparison needs a learned control that is known to work, not
because it is expected to win. M3 is the track.

---

## 6. Experiment specification

The repository rule is that a method comparison states its inputs, outputs, labels and
metrics before the first run. These are those statements.

### ML-A, amortised estimator, simulation only

| Item | Specification |
| --- | --- |
| Input | $P$ scalar power readings in dBm, the $P \times N$ matrix of commanded code words that produced them, one temperature reading in degrees Celsius |
| Output | $N-1$ relative gains in dB and $N-1$ relative phases in radians, channel 0 being the reference |
| Label | the injected $g_n$ and $\psi_n$ from the simulator, available in simulation only |
| Training data | simulator draws, coupling matrix taken from EXP-011 rather than invented, noise level taken from the EXP-005 repeatability floor, phase quantisation matching the chosen bit count |
| Primary metric | root mean square phase error in degrees against $P$, on the same defect draws as B3 and B5 |
| Mandatory negative test | train at one error magnitude and one coupling model, test at another, and report the degradation rather than the best case |

### ML-B, learned drift prior, the central experiment

| Item | Specification |
| --- | --- |
| Input | the last accepted calibration, $2N-2$ reals; elapsed time in hours; temperature now and at the last calibration; a small set of $P$ fresh power readings with their code words; a flag recording whether any connector was touched |
| Output | the updated calibration, $2N-2$ reals |
| Label | a full classical calibration run immediately afterwards, on hardware, which makes the label obtainable without a simulator |
| Primary metric | the smallest $P$ that returns pointing error below the target, against the $4N-4$ the same array needs from scratch |
| Control | recalibrating from scratch, and applying the old calibration unchanged |
| Failure declared if | the required $P$ is not below the from scratch count on held out sessions |

The label mechanism is what makes this track real rather than simulated: the expensive
method supervises the cheap one, on the actual hardware, with no ground truth needed
from a model.

### ML-C, adaptive schedule

| Item | Specification |
| --- | --- |
| Input | the posterior over $g_n$ and $\psi_n$ after $p$ measurements |
| Output | the next code word to command |
| Objective | maximum expected information gain about the $2N-2$ parameters |
| Control | the fixed REV schedule at $K = 3$, and the fixed orthogonal coding schedule |
| Primary metric | the same error against count curve, so it drops straight into the existing benchmark contract |

### ML-D, pattern synthesis by Bayesian optimisation

Run only if $Q^{\,N-1}$ exceeds about 100. Otherwise the result is exhaustive search,
and that is reported as the answer.

**Condition met on 2026-09-18, then reinterpreted on 2026-09-23.** Decision 0003 gives
$Q = 8$ and $N = 4$, so $Q^{\,N-1} = 512$.

That figure was read as making a surrogate worth scheduling. It conflated two costs.
Against an **estimated model**, enumerating 512 states is arithmetic, costs no
measurement and returns the exact optimum, so it is the baseline rather than a problem.
Only in the **model free** arm, where each of the 512 is a physical measurement, is
there anything for a surrogate to improve. The track is therefore a control in that
arm, not a contribution of its own, and the scheduled status is withdrawn. See
`docs/mathematics/inverse-calibration.md` section 5.

---

## 7. The data budget decides the model class

This deserves its own section, because it is usually decided by habit instead.

A full classical calibration at $N = 4$ is of order 12 to 32 measurements. Left running
unattended, a rig completing one calibration every ten minutes produces about 100
labelled recalibration pairs in a week of wall clock time, and each pair carries
$2N-2 = 6$ output dimensions.

One hundred samples of six dimensions does not support a deep network, and any result
claimed from one would be a result about the seed. It supports a Gaussian process or a
small linear Gaussian state model, which is also what the nearest published precedent
uses. **The data budget is a consequence of the hardware, and it selects the model class
before any modelling taste enters.** That is the cleanest example in this project of
hardware determining the algorithm.

It also sets a hardware requirement, running in the opposite direction from the usual
one: the value of Rev A is measured by how many unattended calibrations per hour it can
produce, not by how well it performs in any single one.

---

## 8. Compatibility with what is already decided

| Existing position | Verdict | Reason |
| --- | --- | --- |
| Decision 0001, simulator before hardware | **compatible, and strengthened** | supervised learning needs labels, labels exist only in simulation, so the simulator becomes the training set rather than a checking tool |
| EXP-011, coupling matrix from full wave simulation | **promoted from useful to required** | it is now the training distribution for ML-A, so a wrong coupling model no longer produces a wrong figure, it produces a wrong estimator |
| Two element smallest prototype, `docs/scope.md` section 12 | **incompatible with the ML track** | at $N = 2$ there is one relative phase and one relative gain, so no method can improve on a bound of two real numbers, and the ML track cannot start there |
| Switched line phase shifting at two bits, `docs/hardware/bom-proposal.md` | **tension resolved 2026-09-18** | decision 0003 selects three bits for exactly these two reasons. $Q = 8$ opens the pattern synthesis track, and 45 degree steps stop the B3 baseline being degraded. The bit count is still reported with every result, as `benchmarks/specification.md` requires |
| Acoustic route, option D | **compatible, and self undermining** | measurements become cheap enough to gather thousands, which is exactly what the radio frequency route cannot offer, and that simultaneously removes the premise that measurements are expensive |
| README question 4, "can optimisation cut the number of measurements" | **needs restating** | as written it is not testable at this scale, because section 3 shows the count is already at its bound on first calibration |
| Benchmark primary metric, error against measurement count | **compatible without change** | ML-A, ML-C and the classical baselines all produce that same curve |

---

## 9. What remains undecidable from current evidence

These are not open questions to be worked around. Each one changes the architecture.

| Gate | Question | Settled by | What it decides |
| --- | --- | --- | --- |
| G1 | can phase be measured, or only power | EXP-004, instrument audit | whether the $4N-4$ power only bound applies at all, or whether $2N-2$ complex measurements are available |
| G2 | is drift over hours larger than the repeatability floor | EXP-005 then EXP-010 | **whether the M3 track exists**; if drift hides under the noise floor, the central claim is unmeasurable and must be abandoned rather than reported |
| G3 | element count and phase shifter bit count | **closed 2026-09-18 by decision 0003**: four elements, three bits, so $Q^{\,N-1} = 512$ | M4 has the room the count allows at four elements. **M5 is a control in the model free arm, not a scheduled track**, because 512 states enumerate exactly against an estimated model. Reducing either number reopens this gate and decision 0003 |
| G4 | is coupling significant at the chosen spacing, uncertainty I6 | EXP-011 then S parameter measurement | whether the unknown count is $2N-2$ or $2N^{2}$, which moves every number in section 2 |
| G5 | does the budget allow per element access | costing against the 50 to 70 EUR rule, see `docs/hardware/rev-a-requirements.md` | whether B6 and the unattended dataset are possible |

G2 is the decisive one, and it costs nothing to answer. It is answered with
instruments already owned, before any purchase.

---

## 10. Sources

Full details in `docs/references/bibliography.md`. The claims above rest on:

- REV and its minimum phase state count: Mano and Katagi 1982, with the measurement
  count statement confirmed in arXiv:2504.16107.
- Orthogonal coding: Silverstein 1997.
- Mutual coupling calibration and its single hardware restriction: Aumann, Fenn and
  Willwerth 1989.
- The $4N-4$ generic injectivity bound: Conca, Edidin, Hering and Vinzant 2015.
- Learned calibration from power only measurements: Sarayloo and others 2020, and the
  2024 development of the same idea.
- Gaussian process calibration as the small data precedent: Tambovskiy, Fodor and
  Tullberg 2023.
- Bayesian optimisation as a review reference: Shahriari and others 2016.
