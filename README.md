# AetherArray

A small electronically steered antenna array, and above all a study of what happens
when you try to make it behave the way theory says it should.

- Status: architecture research and feasibility study
- Last reviewed: 2026-08-21

> Nothing is built yet: no array, no measurement bench, no calibration. This
> repository is a public lab notebook. The working frequency, and even the kind of
> wave used, are still open: those choices depend on what the measurement
> environment actually allows, and that has not been audited yet.

---

## The idea in one picture

An antenna array is a set of small antennas fed separately. By adjusting the phase
of the signal sent to each one, you steer the beam without moving anything.

```
   element 0      element 1      element 2      element 3
      |               |              |              |
    phase φ0       phase φ1       phase φ2       phase φ3
      |               |              |              |
      +---------------+--------------+--------------+
                          |
                    same source signal
```

If every element radiates in phase, the beam points straight ahead. Shift the
phases progressively and it tilts. That is the principle behind modern radars and
base station antennas.

In theory it is simple. In practice a real array never points exactly where you ask,
and that is where the whole interest of the project lies.

---

## The ideal model, and why it is wrong

The theoretical behaviour of a linear array is written:

$$
AF(\theta) \;=\; \sum_{n=0}^{N-1} a_n \, e^{\,j\left(n k d \sin\theta \,+\, \phi_n\right)}
$$

Term by term:

- $N$ is the number of elements.
- $a_n$ is the amplitude fed to element $n$, dimensionless.
- $\phi_n$ is the phase we apply to it, in radians. This is our control knob.
- $d$ is the spacing between neighbouring elements, in metres.
- $k = 2\pi/\lambda$ is the wavenumber, in radians per metre. It converts a distance
  into a phase shift: travelling one wavelength rotates the phase by $2\pi$.
- $\theta$ is the observation angle, measured from the perpendicular to the array.
- The term $n k d \sin\theta$ is the natural phase shift caused by the wave from
  element $n$ travelling a different distance to reach the observer.
- $AF(\theta)$ is the resulting field in direction $\theta$, obtained by summing
  every element's contribution.

What the formula says: contributions add up when they arrive in phase and cancel
when they arrive in opposition. To point the beam in direction $\theta_0$ it is
enough to choose:

$$
\phi_n \;=\; -\,n k d \sin\theta_0
$$

In other words, you cancel in advance the natural phase shift caused by geometry.

Some orders of magnitude for a four element array spaced half a wavelength apart:

| Quantity | Approximate value | Meaning |
| --- | --- | --- |
| Beam width | about 25 degrees | with only four elements the beam is not narrow |
| Side lobe level | about -13 dB | there is still energy outside the main beam |
| Array gain | about 6 dB over a single element | doubling the element count adds 3 dB |

Those numbers come from theory and assume everything is perfect.

---

## Why nothing is perfect

Here is the calculation that justifies the whole project on its own.

In ordinary coaxial cable the wave travels at roughly 66 percent of the speed of
light, so with velocity factor $v_f = 0.66$ the wavelength inside the cable at
$f = 2.4$ GHz is:

$$
\lambda_{\text{cable}} \;=\; \frac{v_f\, c}{f} \;=\; \frac{0.66 \times 3\cdot 10^{8}}{2.4\cdot 10^{9}} \;\approx\; 82\ \text{mm}
$$

So one millimetre of cable corresponds to a phase shift of:

$$
\frac{360^{\circ}}{\lambda_{\text{cable}}} \;=\; \frac{360^{\circ}}{82\ \text{mm}} \;\approx\; 4.4^{\circ}\ \text{per millimetre}
$$

**One centimetre of length difference between two cables introduces about 44 degrees
of phase error.** Cutting cables by hand destroys the pattern.

And that is only one error source among several:

| Error source | Origin | Order of magnitude | Correctable? |
| --- | --- | --- | --- |
| Cable length | fabrication | tens of degrees | yes, by calibration |
| Component tolerance | manufacturing spread | a few degrees to a few dB | yes |
| Coupling between neighbouring elements | the antennas see each other | depends on spacing, often significant | partly |
| Thermal drift | temperature change | a few degrees | yes, if you recalibrate |
| Connectors | tightening, wear | a few degrees | yes, but variable |
| Environment | reflections off nearby objects | highly variable | no, you have to control the measurement site |

The combined effect is clear. A useful rule: if the phase errors are random with
standard deviation $\sigma$ in radians, the mean gain degrades as:

$$
\frac{G_{\text{real}}}{G_{\text{ideal}}} \;\approx\; e^{-\sigma^{2}}
$$

For $\sigma = 30^{\circ} \approx 0.52$ rad that is roughly 1.2 dB of loss, and more
importantly a rise in the side lobes, which is usually more annoying than the gain
loss itself.

Translation: an uncalibrated array works, but badly, and unpredictably.

---

## The realistic model

Rather than treating each defect separately, gather them into one complex matrix:

$$
\mathbf{y} \;=\; \mathbf{H}\,\mathbf{x}
$$

- $\mathbf{x} \in \mathbb{C}^{N}$ is the vector of commands we apply, one complex
  value per channel: requested amplitude and phase.
- $\mathbf{y} \in \mathbb{C}^{N}$ is what actually comes out of each element.
- $\mathbf{H} \in \mathbb{C}^{N \times N}$ holds everything: per channel gain and
  phase errors on the diagonal, coupling between elements off the diagonal.

If $\mathbf{H}$ were the identity the system would be perfect. It is not.

Calibrating means measuring $\mathbf{H}$, then applying a corrected command:

$$
\mathbf{x}_{\text{corr}} \;=\; \mathbf{H}^{-1}\,\mathbf{x}_{\text{wanted}}
$$

That is where the project becomes applied mathematics rather than tinkering:
measuring `H` takes measurements, each measurement costs time, and the inversion can
be unstable if the matrix is poorly conditioned.

---

## The real questions

1. **How many measurements does calibration take?** An array with `N` channels has
   at least `N` complex unknowns, and many more if you want the coupling too. Each
   measurement takes time and carries noise.
2. **Can you calibrate without measuring phase?** Many simple setups only measure
   power. Recovering phases from power alone is a classic and non trivial
   mathematical problem.
3. **Is a classical method enough?** Least squares, regularisation, direct
   inversion: these are old, proven and cheap. You need to know how far they go
   before talking about anything else.
4. **Can an optimisation method cut the number of measurements?** This is where
   learning has a real, measurable chance of contributing.
5. **How long does a calibration stay valid?** Rarely addressed, easy to measure,
   and directly useful.

The order is deliberate. The project does not start with machine learning, it starts
with what already works and then looks for where that stops being enough.

---

## The difficulty not to underestimate: measuring

To characterise a radiation pattern you have to be far enough away that the wave has
become planar. The usual minimum distance is:

$$
R \;>\; \frac{2 D^{2}}{\lambda}
$$

where $D$ is the largest dimension of the array and $\lambda$ the wavelength.

Numerical example, four elements at 2.4 GHz spaced 6.25 cm, so $D \approx 0.19$ m
and $\lambda = 0.125$ m:

$$
R \;>\; \frac{2 \times 0.19^{2}}{0.125} \;\approx\; 0.58\ \text{m}
$$

Under a metre, so it fits on a table. But in an ordinary room the signal reflects off
walls, floor, furniture and the operator. Those echoes add to the direct signal and
can produce variations of several decibels, the same order as what we are trying to
measure.

That is the real obstacle. Four routes, none chosen:

| Route | Principle | Advantage | Drawback |
| --- | --- | --- | --- |
| Careful free space measurement | absorbers, distance, differential measurements | realistic | uncertain quality, absorbers cost money |
| Conducted measurement, channel by channel | measure each channel separately through a cable | very repeatable | does not measure radiated coupling |
| Near field measurement | probe moved close to the array, then computed | accurate | needs precise mechanical movement |
| Time domain gating on the analyser | separate the direct path from later echoes | very effective, and free if the instrument supports it | depends on the instrument |
| Lower frequency | everything becomes easier to measure | physically larger array |

There is a fifth route, less obvious, that deserves serious study: **validate the
calibration algorithms on an acoustic array**. At 40 kHz in air the wavelength is
about 8.6 mm, transducers cost a few euros, measurement uses a microphone, and the
entire antenna array theory applies unchanged. The mathematical problem is exactly
the same, the hardware is trivial, and the measurement environment is far easier to
control.

That is not a fallback. It would let the whole algorithmic side be developed and
validated under good conditions, then applied to the RF array knowing it works. It
separates two risks instead of adding them together.

---

## What the project will compare

| Configuration | What it represents |
| --- | --- |
| Ideal simulation | what theory predicts |
| Real system, uncalibrated | what you get for free |
| Classical calibration | inversion, least squares, regularisation |
| Optimised calibration | search for the best setting by optimisation |
| Learning assisted method | if it adds anything |

For each: pointing error, achieved gain, side lobe level, beam width, number of
measurements required, calibration time, and stability over time.

---

## What is still open

1. The working frequency, and even the kind of wave used.
2. The number of elements. Four is probably the right starting compromise.
3. The phase control method: dedicated components, switching, or digital generation.
4. The exact role of the FPGA, which is not a given. A microcontroller may well be
   enough to drive analogue phase shifters.
5. The pattern measurement method.
6. The calibration method.

Point 4 deserves emphasis. An FPGA is only justified for digital beamforming, where
several sampled channels are processed simultaneously. If phase shifting is done by
analogue components, a microcontroller is ample. That choice has to be made on
arguments, not because an FPGA happens to be available.

## What already exists, briefly

| Source | What you find there | What you do not |
| --- | --- | --- |
| Academic | array theory, mutual coupling, calibration methods including power only ones, inverse problems | how many physical measurements each method actually needs, compared |
| Industry | fully documented educational kits, beamforming integrated circuits, application notes | how long a calibration stays valid outside a climate chamber |
| Open source | S parameter processing, Bayesian optimisation, amateur projects that document their failures | a cross validation between a radio frequency array and an acoustic one |

Details in `research/state-of-the-art.md`. Two calibration methods deserve reading
before anything else: the one that needs only power measurements, and the one that
uses coupling between elements as an internal measurement. If the second works at
our scale it would remove the need for a pattern measurement bench entirely, which
would change the project completely.

## How the project will be evaluated

The counted resource is not compute time, it is the **number of physical
measurements**. A measurement means a mechanical move, a settling time and a noisy
acquisition. The associated computation takes milliseconds.

| Criterion | Threshold |
| --- | --- |
| Number of measurements consumed by the method | mandatory next to any calibration result |
| Validation in simulation, where the injected defects are known | mandatory, it is the only place correctness is checkable |
| Measurement repeatability quantified | mandatory, it sets the significance threshold |
| Repetition over several defect draws | mandatory, one draw concludes nothing |
| Measurement conditions and environment recorded | mandatory, room echoes look like lobes |
| Simulated against measured labelling | mandatory |

The reference case is the uncalibrated array. It is what tells you how much
calibration actually buys.

## How to read this repository

| You want to | Go to |
| --- | --- |
| the scope and the questions | `docs/scope.md` |
| the equations, explained | `docs/mathematics/formulation.md` |
| the candidate architectures | `docs/architecture/options.md` |
| the measurement problem | `docs/hardware/inventory-and-needs.md` |
| the calibration methods compared | `benchmarks/methodology.md` and `benchmarks/specification.md` |
| what already exists | `research/state-of-the-art.md` |

## Licence

Undecided at this stage. The repository will contain code, measurements and probably
board design files. Analysis in `LICENSE-NOTES.md`.
