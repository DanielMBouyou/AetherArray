#import "../template.typ": *

= Part VIII. Machine learning <part-viii-machine-learning>

Machine learning is not used because the project needs an AI label. It is used, if gate G2
allows it at all, for one specific thing that physics cannot supply: how this particular array's
state tends to move between calibrations. A physical model knows that a switched line's phase is
$beta thin Delta l$; it does not know by how many degrees channel 2 of this board drifts per degree
Celsius on a Tuesday afternoon, how that drift correlates with channel 3's, or how quickly it
decorrelates. That structure, if it exists, has to be learned from the board's own history.

== 38\. What machine learning does not do

#table(
  columns: (auto, 3.9fr, 10.9fr),
  table.header([], [Statement], [Why]),
  [1], [It does not replace Maxwell's equations], [the likelihood of every measurement is explicit physics, the forward model of `docs/mathematics/inverse-calibration.md` section 2; it is never learned],
  [2], [It does not replace HFSS], [full wave simulation designs and checks the geometry; nothing learned stands in for it],
  [3], [It does not choose the beam on Rev A], [beam synthesis is an exact enumeration of 512 relative states against the estimated array state (section 8.3); decision 0005 withdrew the earlier scheduling of a surrogate pattern synthesis track],
  [4], [It does not perform a first calibration with fewer measurements than identifiability allows], [no method can determine six unknowns from fewer than six readings without prior information; at $N = 4$ the classical routes already sit within a few readings of that floor (section 11.6)],
  [5], [It does not output antenna commands end to end], [nothing learned ever predicts a measurement or a command directly; the learned part predicts where the state probably is],
  [6], [It is not trained on simulated labels and then claimed to solve real drift], [the labels of the central experiment come from full calibrations run on the hardware; the simulation trained estimator ML-A is a control, and its mandatory negative test reports how it degrades out of its training distribution],
  [7], [It does not run in the FPGA], [inference has no hard deadline; the fabric owns timing only (section 19.3)],
  [8], [It does not replace analyser ground truth], [the analyser's per channel complex measurement is the label that supervises the cheap measurements],
)

*Why exhaustive enumeration is a strength, not a weakness.* With 512 relative states, or 820
with the enable bits, the best reachable beam for any criterion, main beam gain, null depth, signal
to interference ratio, can be found exactly in software once the array state is estimated. That
gives the project a known optimum to compare against. A learned or surrogate beamformer would at
best approximate this optimum and would add an error source to the experiment. Only in a model
free comparison, where each of the 512 states is a physical measurement, could a surrogate save
anything, and there it is retained as a control, not as a contribution
(`docs/architecture/ml-calibration.md` section 6, ML-D).

== 39\. What machine learning does

=== 39.1 The learned object

The object of learning is the temporal structure of $vb(H)_t$. For the diagonal model,
represent the identifiable part as a vector of six real numbers, the three relative log gains and
the three relative phases of channels 1 to 3 against channel 0:

$ vb(z)_t = lr(( ln frac(g_1, g_0) \, ln frac(g_2, g_0) \, ln frac(g_3, g_0) \, thick psi_1 - psi_0 \, psi_2 - psi_0 \, psi_3 - psi_0 ))_t in bb(R)^6 $

The phases are angles, so they are taken relative to the previous calibration and kept small,
which avoids the wrap at 360 degrees. A learned prior is then a conditional distribution

$ p_theta lr(( vb(z)_t divides vb(z)_(t - 1) \, vb(z)_(t - 2) \, dots.h \, T_t \, Delta t \, dots.h )) $

with parameters $theta$ fitted on past sessions.

=== 39.2 Learned prior plus physical likelihood

New measurements update the prior by Bayes' rule:

$ p lr(( vb(z)_t divides y_(1 colon k) \, vb(x)_(1 colon k) \, cal(D) )) thick prop thick underbrace(product_(i = 1)^k p lr(( y_i divides vb(z)_t \, vb(x)_i )), "physical likelihood: never learned") thick times thick underbrace(p_theta lr(( vb(z)_t divides cal(D) )), "learned prior") $

#table(
  columns: (auto, 5.9fr, 1.1fr),
  table.header([Factor], [Content], [Origin]),
  [likelihood], [the forward model, complex $sum_n w_n h_n$ for the analyser or power $abs(sum_n w_n h_n)^2$ for the detector, plus a noise model estimated from raw counts and the EXP-005 floor], [explicit physics],
  [prior], [where the state probably is now, given the history], [learned],
  [posterior], [what is believed after $k$ new readings], [Bayes' rule],
)

#aa-figure(num: "10", caption: [prior, likelihood and posterior for one parameter, conceptually. With a good prior,
the posterior reaches the target width with fewer new readings.])[
```text
   probability
       ^
       |            prior p_theta(z | history)               likelihood p(y | z)
       |                 .-.                                     ____
       |                /   \                               ____/    \____     wide: few readings,
       |               /     \                         ____/              \___ power only
       |              /       \                   ____/
       |     ________/         \__________   ____/
       |                     posterior  ~ prior x likelihood
       |                         /\
       |                        /  \      narrower than either: the history pins most of the
       |                       /    \     uncertainty, the new readings pin the rest
       +------------------------------------------------------------------------------> z (one parameter)
```
]

This division is the architectural claim of the project. If the prior is good, few readings are
needed to reach the target accuracy. If the prior is poor but honest about its uncertainty, the
likelihood dominates and more readings are needed: the method degrades towards the from scratch
cost rather than failing. *That property holds only if the prior's uncertainty is calibrated.*
An overconfident prior that is wrong can produce a confident wrong posterior and stop early. The
evaluation must therefore test the prior's predictive coverage on held out sessions, and a
practical safeguard, *\[proposed here\]*, is a residual check: if the posterior predictive
residuals of the new readings exceed what the EXP-005 noise floor allows, the session falls back to
a full calibration and is counted as such.

== 40\. Candidate models

The first model should be simple, for reasons the data decide rather than taste:

#table(
  columns: (2.2fr, 4.5fr),
  table.header([Consideration], [Implication]),
  [dataset size], [of order 100 labelled sessions, an unverified estimate (section 37)],
  [dimensionality], [six outputs per session for the diagonal model],
  [uncertainty], [the stopping rule needs a calibrated posterior, not only a point prediction],
  [interpretability], [a learned temperature coefficient or correlation time is itself a physical finding],
  [temporal correlation], [the data are a time series with irregular intervals],
)

#table(
  columns: (69pt, 5.9fr, 7.1fr, 6.2fr),
  table.header([Model], [What it assumes], [Fits this problem because], [Weak where]),
  [linear Gaussian state space model, inferred with a Kalman filter \[#link(<ref-L30>)[L30]\]], [$vb(z)_t = vb(A) vb(z)_(t - 1) + vb(B) vb(u)_t + vb(q)_t$, Gaussian noise $vb(q)_t$ with covariance growing with $Delta t$; inputs $vb(u)_t$ such as temperature change], [few parameters; exact for complex readings, which are linear in $vb(h)$; extended or unscented variants handle power readings; uncertainty native], [nonlinear or regime changing drift; handling jumps must be modelled separately],
  [autoregressive model], [each parameter regressed on its own recent values and on covariates], [simplest possible baseline; transparent], [point predictions unless wrapped in a probabilistic form],
  [Gaussian process over time and temperature \[#link(<ref-L31>)[L31]\]], [each parameter, or all jointly, is a smooth random function with a covariance kernel whose length scales are learned], [nonparametric with few hyperparameters; uncertainty native; precedent for sparse calibration data \[#link(<ref-A19>)[A19]\] and for temporal gain priors in radio interferometry \[#link(<ref-L23>)[L23]\]], [cost grows with data unless written in state space form, which temporal kernels allow \[#link(<ref-L25>)[L25]\]],
  [neural network], [a flexible function learned from many examples], [none at this data size], [thousands of parameters against hundreds of numbers; uncalibrated uncertainty; any result would mostly reflect the random seed],
)

A large neural network is therefore unjustified initially, and `docs/architecture/ml-calibration.md`
section 7 reaches the same conclusion: the data budget is a consequence of the hardware, and it
selects the model class before modelling taste enters. Which of the first three to use is an
experiment, not a choice to make now (`docs/mathematics/inverse-calibration.md` section 3.2). In
all three, $theta$, the drift dynamics, the temperature coefficients, the kernel length scales,
is fitted on training sessions, for example by maximising the marginal likelihood.

== 41\. Training dataset

Each session would contribute one record built from the schema of section 37:

#table(
  columns: (1.7fr, 5.0fr),
  table.header([Field], [Role]),
  [label $vb(z)_t$], [from a full calibration run on hardware immediately after the cheap measurements, with its own uncertainty],
  [cheap measurements], [the $P$ power readings and the code words that produced them, the input of the sparse recalibration],
  [temperatures], [phase network, detector, die; now and at the last calibration],
  [time], [timestamp and elapsed time since the last calibration],
  [commanded states], [every code word applied],
  [environment and handling], [connector handling flag, operator presence, analyser state],
  [uncertainty], [the label's repeatability, from EXP-005 and EXP-014],
)

The label is itself a measurement with noise. "Equal final accuracy" can only be judged to within
that noise, which is why the session to session repeatability of the full calibration, EXP-014's
criterion, is a prerequisite.

*The split must respect time.* Neighbouring sessions are correlated: they share temperature,
handling history and slow drift. Shuffling sessions at random and splitting them into training and
test sets would place near duplicates on both sides and leak information, producing optimistic
results that would not survive deployment. The split is chronological:

```text
  sessions in time order:  |------- train -------|--- validate ---|---- test ----|
                           early period            later period     final period, untouched until the end
```

Better still is a rolling origin evaluation, training on everything before a point and testing on
the period after it, repeated for several points. Two further leaks to guard against: a connector
handling event on one side of a split boundary that affects the other side, and a test period whose
temperature range lies outside the training range, which must be reported as extrapolation.

== 42\. Baselines

The claim is only as strong as its comparison. The minimum set:

#table(
  columns: (64pt, 7.9fr, 65pt, 4.1fr),
  table.header([Baseline], [Description], [New measurements], [What it shows]),
  [*A*, full recalibration from scratch], [the best classical method at its own minimum: complex per channel readings, or REV at three states, or the fast amplitude only method if verified \[#link(<ref-L7>)[L7]\]], [4 complex, or about 8 to 12 power], [the cost the method must beat],
  [*B*, persistence], [reuse $vb(H)_(t - 1)$ unchanged], [0], [how wrong the old calibration is now; if B already meets the target, there was nothing to recalibrate],
  [*C*, simple temporal model], [the same Bayesian update with a prior that is not learned from the history: the previous state with an uncertainty grown from a fixed rule, such as a random walk whose rate comes from EXP-005 and engineering judgement], [as needed to reach the target], [how much of any saving comes from the Bayesian update and the previous state alone],
  [*D*, uninformative prior with the same update], [the from scratch Bayesian baseline of the stopping rule, section 0.2], [as needed], [isolates the value of the history],
  [*Method*], [learned prior plus physical update], [as needed], [the claim],
  [optional], [learned prior plus active measurement selection], [as needed], [the value of choosing measurements],
)

Baseline C deserves emphasis. A large part of any saving may come simply from starting at the last
calibration with a sensible uncertainty, which needs no learning. The learned prior's contribution
is the difference between the method and C, not between the method and A.

Fairness rules, consistent with `benchmarks/specification.md`: the same sessions for every method;
the same measurement types; the same integration time per reading; every reading counted,
including any used to detect a handling event; baselines run at their own minimum, REV at three
states and not padded; results as curves with spread bands over held out sessions, never a single
number.

The figure that would summarise the learning track:

```text
   estimation error
   (e.g. pointing error, or null depth error)
        ^
        |\
        | \  A / D: from scratch
        |  \
        |   \
        |    \___
        |  \     \______
        |   \  C: previous state, fixed rule   _______ target accuracy delta _______
        |    \___
        |  \     \______
        |   \___  learned prior
        |       \______
        +----------------------------------------------------------------> new measurements k
                  ^            ^                  ^
                  M_req        M_req              M_req
                  (learned)    (C)                (A / D)

   The result is the HORIZONTAL distance at the target accuracy: measurements saved for equal final accuracy.
```

_Conceptual; no curve has been computed or measured._

== 43\. Active measurement selection

Once a posterior exists, the next measurement need not follow a fixed schedule. Bayesian
experimental design chooses it to be as informative as possible about the state \[#link(<ref-L26>)[L26], #link(<ref-L28>)[L28]\]:

$ vb(x)_(k + 1) = arg max_(vb(x) in cal(X)) thick bb(I) lr(( vb(z)_t \; y divides vb(x) \, cal(D)_k )) , wide bb(I) = bb(H) lr(( vb(z)_t divides cal(D)_k )) - bb(E)_y lr([ bb(H) lr(( vb(z)_t divides cal(D)_k \, vb(x) \, y )) ]) $

$bb(I)$ is the mutual information between the state and the outcome of measuring in state
$vb(x)$, and $bb(H)$ is entropy, both in nats. Intuitively: choose the beam state whose
reading is expected to shrink the uncertainty about the array the most. For a measurement linear in
the state, $y = vb(a)^(sf(T)) vb(z) + epsilon.alt$ with noise variance $sigma^2$ and a
Gaussian posterior of covariance $vb(P)$, the gain is

$ bb(I) = frac(1, 2) ln lr(( 1 + frac(vb(a)^(sf(T)) vb(P) thin vb(a), sigma^2) )) $

so the best measurement is the one whose outcome the current belief predicts least well relative
to the noise. Power readings are nonlinear, so the gain must be approximated, by linearising
around the posterior mean or by Monte Carlo. Because the candidate set is the 512 or 820 reachable
states, the maximisation itself is an enumeration, not a search. For Gaussian process models,
greedy mutual information selection is near optimal by a submodularity argument \[#link(<ref-L29>)[L29]\].

This is Bayesian experimental design, which seeks a good *measurement*, not Bayesian
optimisation, which seeks a good *command* \[#link(<ref-A13>)[A13]\]; the repository corrected itself on this once
(`docs/mathematics/inverse-calibration.md` section 4). Active selection is optional and later:
EXP-015 names it, but *nothing is implemented*.

== 44\. Why machine learning becomes useful in the ISAC demonstrator

Section 10bis.5 derives why both ISAC functions depend on the array state and 10bis.6 places the
learning contribution; this section only says what that looks like in a demonstration. The AP-S
demonstrator, if pursued (Part IX), is where the value of calibration, and therefore of cheaper
recalibration, becomes visible to someone who is not an RF engineer.

*Communication mode.* A null placed on an interferer is deep only while the array state is
accurately known (section 9.4).

```text
   null depth on the interferer
   (dB below beam peak)
        ^
   -35  |  ######                          ######
        |  ######                          ######
   -25  |  ######        drift             ######        hypothetical levels, not data;
        |  ######      fills the null      ######        no null has been measured
   -15  |  ######  ######   ######         ######
        +----------------------------------------------------> time
           calibrated   drifted state       recalibrated
                        (stale H_t)         (full, or sparse with learned prior: count M)
```

*Sensing mode.* Hardware drift and environmental change reach the sensing features through the
same product $vb(H)_t vb(R) ( t ) vb(H)_t^(sf(H))$, so drift can be read as a person moving
(section 10bis.5).

The claim the demonstrator can carry is therefore:

#caveat[
Use learned temporal knowledge of RF hardware drift to restore communication and sensing
performance with fewer new physical calibration measurements.
]

That claim is narrower and much stronger than "AI beamforming": it is testable, it has a
non-learned baseline, and its benefit is a count of measurements that a jury can watch being
saved. It also carries a practical condition: drift must occur, or be induced in a controlled and
declared way, within the time of a demonstration. A deliberately warmed beamformer board would be
an induced drift and must be presented as such; a reconnected cable is a jump, not drift.
