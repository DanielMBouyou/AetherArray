# Mathematical formulation

- Status: in progress
- Last reviewed: 2026-08-21

---

## 1. The array factor

For a linear array of `N` identical elements evenly spaced by `d`:

```
AF(θ) = sum over n from 0 to N-1 of:  a_n · exp( j ( n·k·d·sin θ + φ_n ) )
```

- `a_n`: amplitude applied to element `n`, dimensionless.
- `φ_n`: phase applied to element `n`, in radians. This is the command.
- `k = 2π/λ`: wavenumber, in radians per metre. It turns a distance into a phase
  shift.
- `d·sin θ`: path difference between neighbouring elements as seen from direction
  `θ`.
- `n·k·d·sin θ`: accumulated phase shift for element `n`.

Why the complex exponential: it represents a wave as a rotating vector. Adding waves
then becomes adding vectors. When they point the same way the amplitudes add. When
they oppose, they cancel. The whole behaviour of the array sits in that image.

The total radiated pattern is, strictly, the product of the array factor with the
pattern of a single element:

```
total pattern(θ) = single element pattern(θ) × AF(θ)
```

That factorisation assumes every element radiates identically, which is false in the
presence of coupling. It is the first approximation to question.

## 2. Steering

To point in direction `θ0`, choose:

```
φ_n = - n · k · d · sin θ0
```

Interpretation: you deliberately delay each element by exactly enough that all
contributions arrive in phase in the wanted direction.

Two important consequences.

**Grating lobes.** If `d > λ/2` there are other directions where the contributions
also add, and the array radiates parasitic beams as strong as the main one. That is
why the usual spacing is `λ/2`. You can exceed it, provided you know what you are
accepting.

**Beam squint.** The required phase depends on `k`, therefore on frequency. An array
set to point at 30 degrees at one frequency will point slightly elsewhere at
another. Over a narrow band the effect is small, over a wide band it becomes a
problem. The real fix is to apply a time delay rather than a phase shift, which is
more expensive to build.

## 3. Useful quantities

| Quantity | Approximate expression | Interpretation |
| --- | --- | --- |
| Half power beam width | about `0.886 λ / (N·d)` radians, at broadside | the larger the array in wavelengths, the narrower the beam |
| First side lobe level, uniform amplitudes | about -13.2 dB | a fixed value, independent of `N` |
| Array gain | about `10·log10(N)` dB over one element | doubling the element count adds 3 dB |
| Beam broadening off boresight | factor `1/cos θ0` | the beam widens as you steer away from the axis |

The last point is often overlooked: an array steered to 60 degrees has a beam about
twice as wide as at broadside, because its apparent aperture from that direction is
reduced.

## 4. The effect of errors

If the real phases deviate from the intended ones by a random amount with standard
deviation `σ` in radians, the mean gain degrades approximately as:

```
G_real / G_ideal ≈ exp( - σ² )
```

| Phase standard deviation | Gain loss | Effect on side lobes |
| --- | --- | --- |
| 5 degrees | negligible | negligible |
| 15 degrees | about 0.3 dB | slight |
| 30 degrees | about 1.2 dB | noticeable |
| 45 degrees | about 2.7 dB | severe, pattern degraded |

This table is why calibration is a necessity rather than a refinement. It also shows
that gain loss is not the worst of it: the energy lost from the main beam reappears
in the side lobes, which is usually more troublesome in practice.

## 5. The matrix model

Gather every defect into one matrix:

```
y = H · x
```

- `x`: command vector, `N` complex values.
- `y`: signals actually present at the elements.
- `H`: complex `N` by `N` matrix.

Structure of `H`:

- diagonal terms `H_nn` describe the gain and phase specific to each channel,
- off diagonal terms `H_nm` describe coupling between elements `n` and `m`.

If coupling is negligible, `H` is diagonal and calibration reduces to `N`
independent corrections. That is the easy case, and whether it applies has to be
checked rather than assumed. The available electromagnetic simulator can answer that
question before any hardware exists.

## 6. The inverse problem

### Overdetermined case

With `M` measurements and `N` unknowns, if `M > N` the least squares solution is:

```
x_estimated = (A^H A)^(-1) A^H b
```

where `A` is the matrix describing the measurement conditions, `b` the measurement
vector and `A^H` the conjugate transpose.

### Conditioning and regularisation

If `A` is poorly conditioned, meaning some combinations of unknowns are weakly
constrained by the measurements, a small measurement error produces a large
estimation error. The condition number quantifies that risk.

Regularisation adds a constraint:

```
x_estimated = (A^H A + λ I)^(-1) A^H b
```

The `λ I` term stabilises the inversion at the price of a small bias.
Interpretation: a slightly wrong but robust solution beats one that is exact in
theory and absurd in practice. Choosing `λ` is itself a question, handled by cross
validation.

### The power only case

Many simple setups measure only power, so `|y|²`, and lose the phase. Recovering `x`
from magnitudes alone is a known hard problem, called phase retrieval.

A classical method in the antenna array field sidesteps it elegantly: vary the phase
of a single channel and watch the total power. That power varies sinusoidally, and
the position of its maximum gives that channel's phase relative to the sum of the
others. Repeat for each channel and you reconstruct all relative phases without ever
measuring a phase directly.

That is a good example of replacing an expensive instrument with a piece of
reasoning. It deserves study first, including its noise sensitivity and how many
measurements it needs.

## 7. Calibration as optimisation

An alternative to the inverse problem: search directly for the command that
maximises a criterion, without estimating `H`.

```
x* = argmax  f(x)
```

where `f` might be the measured power in one direction, or the negative of the
deviation from a target pattern.

| Method | Expected evaluations | Noise robustness | Note |
| --- | --- | --- | --- |
| Gradient descent | depends, and the gradient is hard to obtain by measurement | poor | badly suited to noisy measurements |
| Simulated annealing | high | good | simple to implement |
| Evolution strategy | high | good | robust but measurement hungry |
| Bayesian optimisation | low | good | designed for expensive evaluations |

The last row is where learning has a clear justification: Bayesian optimisation
builds a probabilistic model of the function being optimised and chooses each
measurement to be as informative as possible. When one measurement takes minutes,
cutting their number by a factor of three is a real and measurable gain.

That is the most defensible way to bring learning into this project, far more so
than training a neural network to predict a pattern.

## 8. Two neighbouring problems, kept apart

They are often conflated and they do not have the same solution.

| Problem | What you are after | What you have to measure |
| --- | --- | --- |
| Calibration | the matrix `H`, meaning the state of the system | measurements informative about each channel |
| Pattern synthesis | the command `x` giving a target pattern | the resulting pattern |

A successful calibration then lets you synthesise any pattern with no further
measurement. A direct optimisation gives a good result for one target, and
everything has to be redone for the next.

That is an interesting trade-off: calibration is expensive once, direct optimisation
is expensive every time. The break even point depends on how many different patterns
you want, and that reasoning will be done explicitly.

## 9. Still to be written

- Modelling coupling from measured S parameters, and its exact link to `H`.
- The embedded element pattern, which replaces the identical element assumption.
- The active impedance model, describing how the impedance seen by one element
  depends on what the others are doing.
- The measurement noise model, without which methods cannot be compared honestly.
