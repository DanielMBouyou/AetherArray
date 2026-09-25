# Calibration as a Bayesian inverse problem

- Status: formalised, nothing implemented
- Last reviewed: 2026-09-23

The learning track stated as physics. `docs/architecture/ml-calibration.md` decided
**where** learning belongs; this document says **what the problem is**, in a form that
can be implemented and argued with.

The short version: the array has a hidden state that drifts, the forward model relating
that state to what we measure is known and explicit, and the job is to infer the state
from as few measurements as possible. History enters as a prior over the state, never
as a replacement for the physics.

---

## 1. Quantities

| Symbol | Meaning | Domain |
| --- | --- | --- |
| $N$ | number of channels, 4 for Rev A | integer |
| $\mathbf{H}_t$ | the array state at time $t$, the hidden quantity | complex matrix |
| $\mathbf{x}_k$ | the commanded beam state of measurement $k$, a 16 bit word | discrete |
| $y_k$ | the measurement returned | real, or complex |
| $\epsilon_k$ | measurement noise | real, or complex |
| $F$ | the forward model, known physics | function |
| $\mathcal{D}$ | the history of previous sessions | data |

---

## 2. Forward model

```math
y_k = F(\mathbf{H}_t, \mathbf{x}_k) + \epsilon_k
```

The commanded word maps to a complex weight per channel. Writing $e_n$ for the enable
bit of channel $n$ and $\phi_n$ for the phase its three bits select:

```math
w_n(\mathbf{x}_k) = e_n(\mathbf{x}_k)\, e^{\,j\phi_n(\mathbf{x}_k)},
\qquad
\phi_n \in \left\{0, \tfrac{\pi}{4}, \tfrac{\pi}{2}, \dots, \tfrac{7\pi}{4}\right\}
```

The eight phases are the nominal values of the three bit switched line network. They are
nominal on purpose: the difference between the nominal phase and the realised one is
part of what $\mathbf{H}_t$ absorbs.

### 2.1 The first model is diagonal, deliberately

```math
\mathbf{H}_t = \operatorname{diag}(h_1, \dots, h_N),
\qquad
h_n = g_n\, e^{\,j\psi_n}
```

$g_n$ is the realised amplitude of channel $n$, dimensionless, and $\psi_n$ its realised
phase in radians. This is the no coupling case, and it is the model to start with
because it is the one whose identifiability is already settled: a common phase rotation
and a common gain scaling are invisible at the sum port, so the identifiable parameter
count is

```math
d = 2N - 2
```

which is six real numbers at $N = 4$. That number governs everything downstream, and
`docs/architecture/ml-calibration.md` section 3 derives it.

The two measurement paths give two forward models over the same state:

```math
F_{\text{complex}}(\mathbf{H}_t, \mathbf{x}_k) = \sum_{n=1}^{N} w_n(\mathbf{x}_k)\, h_n
```

```math
F_{\text{power}}(\mathbf{H}_t, \mathbf{x}_k) = \left| \sum_{n=1}^{N} w_n(\mathbf{x}_k)\, h_n \right|^{2}
```

The first is what the analyser returns and is linear in $\mathbf{H}_t$. The second is
what the on board detector returns and is not. That difference is the whole reason the
two paths have different measurement counts.

### 2.2 The extension, documented and not used yet

With coupling, $\mathbf{H}_t$ is a full $N \times N$ complex matrix, $h_{nm}$ carrying
the coupling from element $m$ into element $n$, and the forward model becomes

```math
F_{\text{complex}} = \mathbf{u}^{\mathsf{T}} \mathbf{H}_t \,\mathbf{w}(\mathbf{x}_k)
```

with $\mathbf{u}$ the combining vector of the divider. The parameter count rises from
$2N-2$ to order $2N^{2}$, which is 32 at $N = 4$, and every measurement count in the
repository has to be recomputed. **This is the extension, not the starting point.**
Uncertainty I6 decides when it becomes necessary, and EXP-011 supplies the coupling
matrix from full wave simulation rather than from a guess.

---

## 3. Inverse objective

The quantity wanted is not a point estimate, it is a posterior:

```math
p\!\left(\mathbf{H}_t \mid y_{1:k}, \mathbf{x}_{1:k}, \mathcal{D}\right)
\;\propto\;
p\!\left(\mathbf{H}_t \mid \mathcal{D}\right)
\prod_{i=1}^{k} p\!\left(y_i \mid \mathbf{H}_t, \mathbf{x}_i\right)
```

Read the two factors carefully, because the division between them is the architectural
claim of this project.

| Factor | What it is | Where it comes from |
| --- | --- | --- |
| $p(y_i \mid \mathbf{H}_t, \mathbf{x}_i)$, the likelihood | the physical forward model of section 2 plus the noise model | **explicit physics, never learned** |
| $p(\mathbf{H}_t \mid \mathcal{D})$, the prior | what the array's own drift history says the state is likely to be now | **learned from history** |

So the learned component predicts **where the state probably is**, and the physics
decides **what that implies for the measurement**. Nothing learned ever predicts a
measurement or a command directly. If the prior is wrong, the likelihood corrects it at
the cost of more measurements; the method degrades rather than failing silently, and
that is the property that makes it worth building.

### 3.1 Sparse recalibration, stated as a stopping rule

The claim under test is not "fewer measurements" in the abstract. It is that the
posterior contracts far enough, far sooner, when the prior carries history. Stop at the
smallest $k$ satisfying

```math
\Pr\!\left( \Delta\theta(\mathbf{H}_t) \leq \delta \;\middle|\; y_{1:k}, \mathbf{x}_{1:k}, \mathcal{D} \right) \;\geq\; 1 - \alpha
```

where $\Delta\theta$ is the pointing error the estimated state implies, $\delta$ the
target, and $\alpha$ the risk accepted. The experiment reports that smallest $k$
against the same quantity for an uninformative prior.

This is the honest form of the measurement count claim, and it is falsifiable: if the
history carries no information, the two values of $k$ coincide.

### 3.2 Prior model class

The data budget, about 100 labelled sessions of six output dimensions, is derived in
`docs/architecture/ml-calibration.md` section 7 and rules out a large network. The
prior is a Gaussian process over time and temperature, or a linear Gaussian state model
with a drift term, and the choice between them is an experiment rather than a taste.

---

## 4. Choosing the next measurement

Active selection maximises expected information gain about the state:

```math
\mathbf{x}_{k+1}^{\star}
= \arg\max_{\mathbf{x} \in \mathcal{X}}
\; \mathbb{I}\!\left(\mathbf{H}_t \,;\, y \mid \mathbf{x}, y_{1:k}\right)
= \arg\max_{\mathbf{x} \in \mathcal{X}}
\left[ \mathbb{H}\!\left(\mathbf{H}_t \mid y_{1:k}\right) - \mathbb{E}_{y}\,\mathbb{H}\!\left(\mathbf{H}_t \mid y_{1:k}, \mathbf{x}, y\right) \right]
```

where $\mathbb{I}$ is mutual information and $\mathbb{H}$ is entropy.

**This is Bayesian experimental design, not Bayesian optimisation.** The distinction is
not pedantry and the repository has already had to correct itself once on it:

| | Objective | Answer sought |
| --- | --- | --- |
| Bayesian experimental design, used here | reduce uncertainty about $\mathbf{H}_t$ | a good **measurement** |
| Bayesian optimisation, not used here | improve on the best observed value of some $f$ | a good **command** |

The candidate set $\mathcal{X}$ is the reachable beam states, which for Rev A is finite
and small, so the maximisation is an enumeration and not a search.

---

## 5. Beam synthesis is a separate problem, and for Rev A it is exact

Once a state estimate exists, choosing the command is downstream and independent:

```math
\mathbf{x}^{\star} = \arg\max_{\mathbf{x} \in \mathcal{X}} \; U\!\left(\hat{\mathbf{H}}_t, \mathbf{x}\right)
```

with $U$ the pattern criterion, pointing error or gain in the wanted direction.

For Rev A, with three phase bits and one channel taken as the reference,

```math
\left|\mathcal{X}\right| = 8^{\,N-1} = 8^{3} = 512
```

**512 states is an enumeration, not an optimisation.** Evaluating all of them against an
estimated $\hat{\mathbf{H}}_t$ is arithmetic, it costs no measurement, and it returns
the exact optimum over the reachable set. There is no surrogate to build and no search
to tune.

### Correction to an earlier position

`docs/architecture/ml-calibration.md` recorded that crossing 512 states made the
pattern synthesis track worth scheduling. That conflated two different costs.

| Setting | Cost of enumerating 512 | Status |
| --- | --- | --- |
| Against an estimated model | 512 arithmetic evaluations | **the exact baseline for Rev A** |
| Directly on hardware, model free | 512 physical measurements | expensive, and the arm a surrogate could improve |

So a surrogate method has a role only in the **model free** comparison arm, as a control
against which calibration plus enumeration is measured. It is not a contribution track
of its own, and the earlier "scheduled" status is withdrawn.

---

## 5.1 How the numbers get here

The forward model above consumes complex per channel transfers, and those arrive
through one path: `tools/rfkit`, described in `docs/architecture/rf-data-layer.md`.
It turns Touchstone exports from the electromagnetic solver, the circuit simulator
and the analyser into the diagonal state of section 2.1, keeping the raw complex
values and the provenance of every trace.

Three of its guarantees matter to this document specifically. Traces are compared
only over the frequency range they share, so a likelihood is never evaluated
against an extrapolated measurement. Phase differences are taken on the circle, so
a channel near the wrap point does not acquire a spurious 360 degrees. And the
`ArrayState` object carries the full coupling matrix form as well as the diagonal
one, so the extension in section 2.2 needs no change of data structure.

## 6. What this formalisation commits the hardware to

Each of these already exists in `docs/architecture/control-architecture.md`, and this
section records why the inverse problem needs it.

| Requirement | Which term needs it |
| --- | --- |
| The commanded word recorded per measurement, not inferred | $\mathbf{x}_k$ enters the likelihood directly; a wrong command is a wrong model |
| A deterministic, recorded settling delay | an unsettled measurement is a sample of a different $\mathbf{H}$ |
| Timestamps from one clock | $\mathcal{D}$ is indexed by time, and the drift prior is a function of it |
| Temperature with every record | the prior is conditioned on temperature, not on time alone |
| Raw converter counts kept | the noise model $\epsilon_k$ is estimated from data, and scaling first discards the information needed to do it |
| Connector handling flagged | uncertainty I14; handling is a jump in $\mathbf{H}_t$, not drift, and must be modelled as such or excluded |
