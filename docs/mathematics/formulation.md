# Mathematical formulation

- Status: in progress
- Last reviewed: 2026-08-21

---

## 1. The array factor

For a linear array of $N$ identical elements evenly spaced by $d$:

```math
AF(\theta) = \sum_{n=0}^{N-1} a_n \, e^{\,j\left(n k d \sin\theta \,+\, \phi_n\right)}
```

| Symbol | Meaning | Unit |
| --- | --- | --- |
| $a_n$ | amplitude applied to element $n$ | dimensionless |
| $\phi_n$ | phase applied to element $n$, the command | rad |
| $k = 2\pi/\lambda$ | wavenumber, converts a distance into a phase shift | rad/m |
| $d$ | spacing between neighbouring elements | m |
| $\theta$ | observation angle, from the array normal | rad |
| $n k d \sin\theta$ | path difference expressed as a phase shift | rad |

Why the complex exponential: it represents a wave as a rotating vector. Adding waves
then becomes adding vectors. When they point the same way the amplitudes add, when
they oppose they cancel. The whole behaviour of the array sits in that image.

The total radiated pattern is, strictly, the product of the array factor with the
pattern of a single element:

```math
P(\theta) = P_{\text{elem}}(\theta) \cdot AF(\theta)
```

That factorisation assumes every element radiates identically, which is false in the
presence of coupling. It is the first approximation to question.

## 2. Steering

To point in direction $\theta_0$, choose:

```math
\phi_n = -\,n k d \sin\theta_0
```

Interpretation: you deliberately delay each element by exactly enough that all
contributions arrive in phase in the wanted direction.

Two important consequences.

**Grating lobes.** The array factor repeats whenever the inter element phase
advances by a full turn, that is when

```math
k d \left(\sin\theta - \sin\theta_0\right) = 2\pi m, \qquad m \in \mathbb{Z}
```

has a solution with $|\sin\theta| \le 1$ other than $m = 0$. Avoiding that for every
steering angle requires

```math
\frac{d}{\lambda}  <  \frac{1}{1 + |\sin\theta_0|}
```

which gives the familiar $d \le \lambda/2$ for full hemispheric steering. You can
exceed it, provided you know what you are accepting.

**Beam squint.** The required phase depends on $k$, therefore on frequency. An array
set for $\theta_0$ at frequency $f_0$ points, at frequency $f$, towards

```math
\sin\theta = \frac{f_0}{f}\,\sin\theta_0
```

Over a narrow band the effect is small, over a wide band it becomes a problem. The
real fix is a true time delay rather than a phase shift, which is more expensive to
build.

## 3. Useful quantities

| Quantity | Expression | Interpretation |
| --- | --- | --- |
| Half power beam width at broadside | $\Delta\theta_{3\text{dB}} \approx \dfrac{0.886\,\lambda}{N d}$ | the larger the array in wavelengths, the narrower the beam |
| First side lobe, uniform amplitudes | $\approx -13.2$ dB | a fixed value, independent of $N$ |
| Array gain | $G \approx 10\log_{10} N$ dB over one element | doubling the element count adds 3 dB |
| Broadening off boresight | $\Delta\theta(\theta_0) \approx \dfrac{\Delta\theta_{3\text{dB}}}{\cos\theta_0}$ | the beam widens as you steer away from the axis |

The last row is often overlooked: an array steered to $60^{\circ}$ has a beam about
twice as wide as at broadside, because its projected aperture is reduced by
$\cos\theta_0$.

## 4. The effect of errors

If the realised phases deviate from the intended ones by independent random errors
with standard deviation $\sigma$ in radians, the mean gain degrades as:

```math
\frac{\mathbb{E}\left[G_{\text{real}}\right]}{G_{\text{ideal}}}  \approx  e^{-\sigma^{2}}
```

| $\sigma$ | Gain loss | Effect on side lobes |
| --- | --- | --- |
| $5^{\circ}$ | negligible | negligible |
| $15^{\circ}$ | $\approx 0.3$ dB | slight |
| $30^{\circ}$ | $\approx 1.2$ dB | noticeable |
| $45^{\circ}$ | $\approx 2.7$ dB | severe, pattern degraded |

This table is why calibration is a necessity rather than a refinement. It also shows
that gain loss is not the worst of it: the energy lost from the main beam reappears
in the side lobes, which is usually more troublesome in practice.

## 5. The matrix model

Gather every defect into one complex matrix:

```math
\mathbf{y} = \mathbf{H}\,\mathbf{x}, \qquad
\mathbf{H} \in \mathbb{C}^{N \times N}
```

Structure of $\mathbf{H}$:

```math
H_{nm} =
\begin{cases}
g_n\, e^{\,j\psi_n} & \text{if } n = m, \quad \text{channel gain and phase error} \[4pt]
c_{nm} & \text{if } n \neq m, \quad \text{coupling between elements } n \text{ and } m
\end{cases}
```

If coupling is negligible, $\mathbf{H}$ is diagonal and calibration reduces to $N$
independent corrections. That is the easy case, and whether it applies has to be
checked rather than assumed. The available full wave simulator can answer that
question before any hardware exists.

## 6. The inverse problem

### Overdetermined case

With $M$ measurements and $N$ unknowns, if $M > N$ the least squares solution is:

```math
\hat{\mathbf{x}} = \left(\mathbf{A}^{H}\mathbf{A}\right)^{-1}\mathbf{A}^{H}\,\mathbf{b}
```

where $\mathbf{A}$ describes the measurement conditions, $\mathbf{b}$ holds the
measurements and $\mathbf{A}^{H}$ is the conjugate transpose.

### Conditioning and regularisation

If $\mathbf{A}$ is poorly conditioned, a small measurement error produces a large
estimation error. The condition number

```math
\kappa(\mathbf{A}) = \frac{\sigma_{\max}(\mathbf{A})}{\sigma_{\min}(\mathbf{A})}
```

quantifies that risk, where $\sigma_{\max}$ and $\sigma_{\min}$ are the largest and
smallest singular values.

Tikhonov regularisation adds a constraint:

```math
\hat{\mathbf{x}}_{\mu} = \left(\mathbf{A}^{H}\mathbf{A} + \mu \mathbf{I}\right)^{-1}\mathbf{A}^{H}\,\mathbf{b}
```

The term $\mu \mathbf{I}$ stabilises the inversion at the price of a small bias.
Interpretation: a slightly wrong but robust solution beats one that is exact in
theory and absurd in practice. Choosing $\mu$ is itself a question, handled by cross
validation.

### The power only case

Many simple setups measure only power, so $|y|^{2}$, and lose the phase. Recovering
$\mathbf{x}$ from magnitudes alone is a known hard problem, called phase retrieval.

A classical method in this field sidesteps it. Sweep the phase $\varphi$ of a single
channel $n$ while the others stay fixed. Writing $S = \sum_{m \neq n} y_m$ for the
sum of the other channels, the total received power is:

```math
P(\varphi) = \left| S + |y_n|\, e^{\,j(\psi_n + \varphi)} \right|^{2}
= |S|^{2} + |y_n|^{2} + 2\,|S|\,|y_n|\,\cos\!\left(\psi_n + \varphi - \arg S\right)
```

The power varies sinusoidally with $\varphi$, and the position of its maximum gives
$\psi_n$ relative to $\arg S$. Repeat for each channel and you reconstruct every
relative phase without ever measuring a phase directly.

That is a good example of replacing an expensive instrument with a piece of
reasoning. It deserves study first, including its noise sensitivity and how many
measurements it needs.

## 7. Calibration as optimisation

An alternative to the inverse problem: search directly for the command maximising a
criterion, without estimating $\mathbf{H}$.

```math
\mathbf{x}^{\star} = \arg\max_{\mathbf{x}}   f(\mathbf{x})
```

where $f$ might be the measured power in one direction, or the negative deviation
from a target pattern.

| Method | Expected evaluations | Noise robustness | Note |
| --- | --- | --- | --- |
| Gradient descent | depends, and the gradient is hard to obtain by measurement | poor | badly suited to noisy measurements |
| Simulated annealing | high | good | simple to implement |
| Evolution strategy | high | good | robust but measurement hungry |
| Bayesian optimisation | low | good | designed for expensive evaluations |

The last row is where learning has a clear justification: Bayesian optimisation
builds a probabilistic surrogate of $f$ and picks each measurement to maximise an
acquisition function, so it is built for the case where one evaluation is expensive.
When a measurement takes minutes, cutting their number by a factor of three is a
real and measurable gain.

That is the most defensible way to bring learning into this project, far more so
than training a network to predict a pattern.

## 8. Two neighbouring problems, kept apart

They are often conflated and they do not have the same solution.

| Problem | What you are after | What you have to measure |
| --- | --- | --- |
| Calibration | the matrix $\mathbf{H}$, the state of the system | measurements informative about each channel |
| Pattern synthesis | the command $\mathbf{x}$ giving a target pattern | the resulting pattern |

A successful calibration then lets you synthesise any pattern with no further
measurement. A direct optimisation gives a good result for one target, and
everything has to be redone for the next.

That is an interesting trade-off: calibration is expensive once, direct optimisation
is expensive every time. The break even point depends on how many different patterns
you want, and that reasoning will be done explicitly.

## 9. Still to be written

- Modelling coupling from measured S parameters, and its exact link to $\mathbf{H}$.
- The embedded element pattern, which replaces the identical element assumption.
- The active impedance model, describing how the impedance seen by one element
  depends on what the others are doing.
- The measurement noise model, without which methods cannot be compared honestly.
