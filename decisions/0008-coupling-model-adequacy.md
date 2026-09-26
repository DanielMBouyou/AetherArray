# 0008. Gate G4: the diagonal state stays only if neglecting coupling costs less than the budget

- Status: accepted; the criterion is fixed and no coupling data exist
- Date: 2026-09-26
- Scope: gate G4 and uncertainty I6, EXP-011, the full matrix extension in `docs/mathematics/inverse-calibration.md` section 2.2, and `tools/rfkit/coupling.py`

## Question

Before any coupling has been simulated or measured, by what test, derived from what
coupling does to the calibrated beam, does Rev A keep the diagonal array state, and when
must it promote coupling into the calibration model?

## Context

Gate G4 is written as "is coupling significant at the chosen spacing", settled by EXP-011
and then by measurement, and deciding whether the unknowns number $2N-2$ or order
$2N^{2}$. Nothing defines "significant". Decision 0007 derived a budget for everything
except coupling, and said so.

What the diagonal state absorbs was settled in decision 0007: the forward model uses
nominal state phases, and one complex number per channel absorbs whatever does not
depend on the commanded state. Coupling is exactly the kind of error that can depend on
the state, because the contribution of element $m$ to element $n$ carries the relative
phase of their commands.

Decision 0003's two board split makes the two coupling mechanisms separable: the
antenna board and the beamforming board meet at four element connectors, and each can be
characterised on its own at that plane.

## The quantities

| Quantity | What it is | Where it is obtained | Enters G4 |
| --- | --- | --- | --- |
| $\mathbf{S}_A$ | the antenna board's $4 \times 4$ scattering matrix at the element connectors, other ports matched | simulation first, measurement through the connectors later | yes, the subject |
| output match $\Gamma_{B,n}(k)$ | reflection at beamformer output $n$ with channel $n$ in state $k$ | conducted, part of the per channel measurement | yes, through $\mathbf{S}_{Bo}$ |
| output isolation $X_{nm}$ | transmission from output $m$ to output $n$, common port terminated | conducted pairs | yes, through $\mathbf{S}_{Bo}$ |
| forward crosstalk | channel $n$'s transfer changing with channel $m$'s state | conducted, cycling a neighbour's state | **no**: a state dependent diagonal error, judged under decision 0007 |
| embedded element patterns | far field of each port excited alone, others matched | simulation only | checks the approximation below |

**Antenna port mutual coupling** is the off diagonal of $\mathbf{S}_A$: radiative, set by
the geometry. **Beamformer path crosstalk** is a property of the other board: its reverse
part acts only together with $\mathbf{S}_A$, through the waves the antennas reflect.

## The coupled forward model

For the waves $\mathbf{t}(s)$ the beamformer delivers into matched loads in commanded
state $s$:

```math
\mathbf{a}(s) = \left(\mathbf{I} - \mathbf{S}_{Bo}(s)\,\mathbf{S}_A\right)^{-1}\mathbf{t}(s),
\qquad
\mathbf{e}(s) = \left(\mathbf{I} - \mathbf{S}_A\right)\mathbf{a}(s),
\qquad
E(u, s) = \mathbf{v}(u)^{\mathsf{T}}\,\mathbf{e}(s)
```

| Symbol | Meaning |
| --- | --- |
| $\mathbf{S}_{Bo}(s)$ | beamformer reverse path: $\Gamma_{B,n}(s_n)$ on the diagonal, $X_{nm}$ off it |
| $\mathbf{a}(s)$ | waves actually incident on the antennas |
| $\mathbf{e}(s)$ | radiating currents |
| $v_m(u)$ | $e^{\,j m k d u}$, with $u = \sin\theta$ and element 0 at the origin |

The middle equation is the canonical minimum scattering approximation, bibliography
[A23] and [A24]: an antenna radiates according to its port current, the difference of
incident and reflected waves. It is exact for no real patch, which is why the simulation
stage also uses the solver's embedded element patterns, where the field is
$E(u,s) = \sum_n g_n(u)\, a_n(s)$ with no approximation.

The diagonal model is the same array with the off diagonal parts removed, one state
independent complex factor per channel, and the array's average embedded element
pattern $\hat{f}(u)$:

```math
E_d(u, s) = \hat{f}(u)\,\mathbf{v}(u)^{\mathsf{T}} \operatorname{diag}(\mathbf{h})\,\mathbf{M}_0(s)\,\mathbf{t}(s)
```

$\mathbf{M}_0$ keeps only the diagonal mismatch terms, so with no coupling $\mathbf{h} = 1$
and $E_d = E$ exactly: whatever remains is due to coupling alone. $\hat{f}$ comes from
EXP-011 itself, needs no calibration and adds no unknown. Without it, the part of every
element's scan dependence that is common to all of them would be charged to coupling.

## What the model showed before any data

Four findings, from the model and from synthetic matrices only. Each shaped the
criterion.

**1. A calibration residual cannot detect coupling.** When coupling does not depend on
the state, a probe calibration at one direction fits the diagonal model exactly: the
residual in the tests is of order $10^{-16}$. It becomes non-zero only through state
dependent beamformer reflections. The error from coupling appears when the beam is
steered away from where the calibration looked, so G4 has to be judged on steered
beams, not on how well a calibration fits.

**2. A single raw coupling number cannot decide G4.** On a synthetic matched uniform
array with nearest neighbour coupling of $-25$ dB, the broadside calibration's pointing
error ranges from 0.38 to 1.27 of the budget as the phase of the coupling varies. Same
magnitude, opposite verdicts.

**3. A single number can guarantee something narrower.** If every channel's coupled
current differs from its own diagonal term by at most

```math
\rho = \max_{n,s} \frac{\sum_{m \ne n} \lvert C_{nm}(s)\, t_m(s) \rvert}{\lvert C_{nn}(s)\, t_n(s) \rvert},
\qquad \mathbf{C} = (\mathbf{I} - \mathbf{S}_A)(\mathbf{I} - \mathbf{S}_{Bo}\mathbf{S}_A)^{-1}
```

then the phase error is at most $\arcsin\rho$, and decision 0007's worst pattern bound
passes when $\rho \le \sin T = 0.040$: an aggregate of $-28$ dB, or $-34$ dB per
neighbour for an inner element. That bounds the **unfitted** comparison of the full
operator with its own diagonal, not the calibrated model, and it is conservative: on the
synthetic chart, full propagation passes at every coupling phase down to $-27$ dB while
the screen clears only at $-35$ dB. **Only full propagation is defensible**. The screen is
reported and never decides.

**4. Coupling is structured, not random.** A uniform array's coupling is reciprocal and
close to Toeplitz, deterministic, and correlated across elements. Treating it as
independent random terms would be the wrong model. The evaluation uses the actual complex
matrix, all eight command origins and every judged angle, so the coherent worst case is
the one the hardware's own phases produce.

## Options considered

### Option A: a raw coupling limit in decibels

Simple, and finding 2 shows it decides nothing. Rejected.

### Option B: the single number screen as the criterion

Sufficient, so it cannot pass a bad array. It would reject arrays that pass by several
decibels, and it bounds the wrong comparison. Rejected as a criterion, kept as a
descriptor.

### Option C: a model adequacy test by full propagation

Judge the error the diagonal model makes, once calibrated, on every steered beam that
matters, against the budget decision 0007 already uses. Chosen.

### Option D: promote the full matrix now, whatever EXP-011 shows

Removes the question at the price of the unknown count, and of every measurement count
in `docs/architecture/ml-calibration.md` section 2, before knowing whether that price is
necessary. The test is available before any hardware exists, so paying in advance buys
nothing. Rejected.

## Comparison

| Criterion | A, raw limit | B, screen | C, propagation | D, full matrix now |
| --- | --- | --- | --- | --- |
| Tied to a downstream consequence | no | through a bound | directly | not applicable |
| Can pass a bad array | yes | no | no, within the model | no |
| Rejects good arrays | sometimes | by several dB | no, within the model | always pays the cost |
| Needs the full complex matrix | no | yes | yes | yes |
| Decidable before hardware | yes | yes | yes, from simulation | yes |

## Evidence

No experimental evidence. The derivation is above. The numerical checks are in
`tools/rfkit/tests/test_coupling.py`, on synthetic matrices: exactness with no
coupling, exactness of the known coupling model, the zero residual of finding 1, the
phase dependence of finding 2, the screen's bound of finding 3, and agreement of the two
far field routes when the patterns are built from the model. External sources:
[A23] and [A24], bibliographic details and abstracts only. The synthetic chart is
produced by `python -m rfkit.cli g4-chart` and is **not a prediction of EXP-011**: a
matched, uniform, nearest neighbour array is an idealisation.

## Decision

### The budget

The same policy as decision 0007, with **a separate allocation**: $\eta_c = 0.10$ of the
quantisation floor's error variance. Separate, because the error left by neglecting
coupling is a real error in the calibrated beam and it adds to the design errors decision
0007 already budgets, rather than replacing any of them. Together they may add at most
0.20 of the floor variance: pointing spread up by at most 9.5 per cent, coherent gain loss
and the error sidelobe floor by at most 20 per cent.

At each judged point, the beam of the calibrated diagonal model is compared with the
coupled beam:

```math
\delta\theta^{2} \le \eta_c\, \sigma_{\theta,q}^{2}(\theta_0),
\qquad
L\!\left(1 + \boldsymbol{\epsilon}\right) \le \eta_c\, L_q
```

$\delta\theta$ is the exact difference of the two beam maxima, $\sigma_{\theta,q}(\theta_0)$
the quantisation pointing spread at the steering angle, $\boldsymbol{\epsilon}$ the
relative error of the equivalent element currents, $L$ the exact coherence loss of
decision 0007, and $L_q$ = 0.167 dB the floor's.

### What is judged

| Item | Fixed value | Where |
| --- | --- | --- |
| frequencies | every data point inside band 57a, both edges and $f_0$ | `rfkit.coupling.evaluate` |
| steering angles | $-45$ to $+45$ degrees in one degree steps, the benchmark set inside it | `rfkit.thresholds.G4` |
| command origins | all eight | same |
| calibration | complex probe readings at broadside over the rotation family: all channels at state 0, then each channel through its other seven states, 29 configurations | `rfkit.coupling.calibration_states` |
| best diagonal | the least squares state independent factor for the currents over exactly the judged states | `rfkit.coupling.evaluate` |
| guard, measured data | one matrix with every coupling term inflated by $U$, and 32 reciprocal perturbations of magnitude $U$ at phases from seed 20260926 | `rfkit.coupling.guard_matrices` |

### The rules, fixed before any data

| Outcome | Condition |
| --- | --- |
| **PASS** | the broadside calibration keeps every judged beam inside the budget, the outcome is the same across the mesh passes or across every guard matrix, and the far field route has been checked |
| **FAIL** | even the best diagonal leaves a judged beam outside the budget, stably, with the route checked |
| **INTERMEDIATE** | anything else: the best diagonal holds but the broadside calibration does not find it, or the outcome changes across passes or within the uncertainty, or the route is unchecked, or the two routes disagree |
| **UNRESOLVED** | the data do not cover band 57a, the matrix is not passive within its tolerance, or a required input is missing |

The simulation stage needs the last two adaptive passes and the embedded element
patterns. When the two far field routes disagree, the embedded route governs that stage
and the measured stage, which can only use the minimum scattering route, is capped at
intermediate. The measured stage needs the analyser's expanded uncertainty $U$ of each
S term, the beamformer's reverse path, and Stage 1's record of whether the routes agreed.
The observed reciprocity defect sets a floor under $U$: a measurement cannot claim an
uncertainty smaller than half the asymmetry it shows. One further rule waits on EXP-005
Phase B: if the calibration residual exceeds the repeatability floor, a pass becomes
intermediate, because the diagonal likelihood is then misspecified at the noise level.

### What follows from each outcome

**PASS.** The diagonal state remains the Rev A calibration baseline. Nothing reopens.

**INTERMEDIATE.** The evidence required depends on the reason, and is named now:

| Reason | Required before the gate closes |
| --- | --- |
| best diagonal holds, broadside calibration does not | judge a calibration that could find it, several probe directions or conducted labels corrected with $\mathbf{S}_A$, by the same rules |
| outcome changes across mesh passes | further adaptive passes until two agree |
| outcome changes within the uncertainty | reduce $U$ by a better calibration chain or repeated measurement, then rerun |
| routes disagree, or route unchecked | the embedded patterns; for the measured stage, a pattern measurement, which needs the deferred positioner |
| residual above the repeatability floor | inflate the noise model of `docs/mathematics/inverse-calibration.md` section 3, or promote as for a fail |

**FAIL.** The promotion is staged, cheapest first:

1. **Known static coupling.** The forward model becomes
   $E = \mathbf{v}^{\mathsf{T}}\mathbf{C}(s)\operatorname{diag}(\mathbf{h})\,\mathbf{t}(s)$
   with $\mathbf{C}$ from the measured stage, frozen. The unknowns stay $2N-2$, so the
   counts of `docs/architecture/ml-calibration.md` section 2 survive, provided
   $\mathbf{C}$ does not drift. It is judged by the same rules, `evaluate(..., model=...)`,
   against a second independent matrix: the simulation against the measurement, or two
   measured sessions at different temperatures.
2. **Full matrix.** If the known coupling model fails that test, coupling is estimated,
   the unknowns rise to order $2N^{2}$, and these reopen: `ml-calibration.md` section 2
   and gate G4's row, decision 0002's headroom analysis for track M3, EXP-012, EXP-013's
   training data, EXP-015, the diagonal default in `rfkit.state`, and decision 0007,
   whose derivation assumes the diagonal state.

## Consequences

- G4 has a criterion written before its data, and it is executable:
  `python -m rfkit.cli g4`.
- EXP-011 has a protocol, `experiments/EXP-011-coupling-model-adequacy.md`, that says
  exactly which files, ports, planes, grids and metadata each stage must supply.
- The simulation stage can settle G4 before fabrication, when there is still time to
  react to it, though not by changing the geometry here.
- A failure does not automatically cost the unknown count: the known coupling model is
  tried first.
- Work created: an HFSS far field export converted into the documented pattern container,
  and the beamformer measurements packed into theirs.

## Known limitations

- **The best diagonal is least squares on the currents, not a minimax on pointing.** On
  the synthetic chart it sometimes points worse than the broadside calibration, 1.15
  against 1.11 of the budget. A fail is therefore defined operationally, not as the
  nonexistence of any diagonal that passes.
- The minimum scattering approximation is checked only in simulation; the measured stage
  inherits that check.
- Forward crosstalk is excluded from G4 and judged under decision 0007.
- One polarisation and one plane, the one containing the array axis. Cross polar
  behaviour is not judged.
- The probe is assumed in the far field at broadside, 0.55 m at 2.44 GHz by decision 0004.
- Commands are the nominal ones at $f_0$; band edge dispersion of the lines belongs to
  decision 0007.
- No HFSS far field file reader exists; the container it must fill is defined.

## Conditions for reopening

- The steering set, the bit count, the element count or the spacing changes.
- The calibration method changes from a probe method, for example to the mutual coupling
  method B6 as the primary: the calibration model inside the test then changes.
- The probe position of the bench changes from broadside.
- A numeric pointing target is recorded, which reopens decision 0007 and this with it.
- EXP-007 contradicts the error propagation model.
- The embedded patterns show the minimum scattering route inadequate for this array.
