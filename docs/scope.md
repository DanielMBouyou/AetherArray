# Scope

- Status: in progress
- Last reviewed: 2026-08-21

## 1. What problem are we solving

Build an electronically steered antenna array, measure the gap between its real
behaviour and its theoretical behaviour, and determine which calibration method
closes that gap at the lowest cost, where cost is measured mainly in physical
measurements.

## 2. Why it is interesting

- It shows, dramatically, the gap between a clean model and physical reality. One
  centimetre of cable is enough to ruin a pattern.
- It combines electronics, RF, signal processing, optimisation and metrology in one
  object.
- It poses a genuine inverse problem: recover hidden parameters from indirect, noisy
  measurements.
- The question of how many measurements are needed is exactly where an optimisation
  or learning method can contribute, and that contribution is directly measurable.
- The skills involved are sought after in radar, communications and instrumentation.

## 3. Formulation

The real system is described by:

```math
\mathbf{y} = \mathbf{H}\,\mathbf{x}
```

$\mathbf{x}$ is the vector of commands applied to the channels, $\mathbf{y}$ what
actually comes out, and $\mathbf{H} \in \mathbb{C}^{N \times N}$ a complex matrix
holding the gain errors, the phase errors and the coupling.

Calibration means estimating `H` from a limited number of measurements, then
deriving the corrected command. Optimisation means finding the command that gives
the pattern closest to a target, which is not quite the same thing and the two are
kept distinct.

Full detail in `docs/mathematics/formulation.md`.

## 4. What already exists

See `research/state-of-the-art.md`:

- An old and solid literature on antenna arrays, patterns, mutual coupling and
  manufacturing errors.
- Proven calibration methods, some of which use only power measurements.
- Fully documented commercial educational phased array kits, which show a realistic
  architecture.
- A recent literature applying Bayesian optimisation to calibration and to tuning
  systems that are expensive to evaluate.

## 5. Families to compare

| Family | Description | Measurement cost |
| --- | --- | --- |
| No calibration | apply theory as is | none |
| Channel by channel calibration | measure each channel separately | proportional to the channel count |
| Phase rotation method | vary one channel's phase and watch total power | several measurements per channel, but no phase measurement needed |
| Least squares inversion | estimate the full matrix | depends on the measurement count |
| Regularised least squares | same, with a stability constraint | same |
| Direct pattern optimisation | search for the command giving the best pattern, without estimating the matrix | many evaluations |
| Bayesian optimisation | choose each measurement to be maximally informative | designed to reduce measurement count |
| Learned method | predictive model of drift or of missing parameters | depends |

## 6. What resources we have

A vector network analyser, an oscilloscope and a function generator whose models are
unknown, a full electromagnetic and circuit simulation stack with scripting,
microcontrollers for control and positioning, FPGA boards if the digital route is
chosen, and a GPU machine for optimisation. Detail in
`docs/hardware/inventory-and-needs.md`.

The electromagnetic simulator matters more than usual here: it can produce a
physically grounded coupling matrix, so the simulation study rests on physics rather
than on an invented model.

## 7. What we are missing

- A way to measure a radiation pattern under decent conditions: absorbers, an
  angular positioner, a controlled environment.
- Commandable phase shifters, unless the digital route is chosen.
- Possibly several coherent receive channels, if digital beamforming is pursued.
- Antennas, which can be fabricated on a printed circuit board.

## 8. Benchmarks

See `benchmarks/methodology.md` and `benchmarks/specification.md`. Principle: compare
calibration methods on the same array, with the same defects, counting the
measurements each consumes.

Important point of method: a large part of the comparison can be done **in
simulation**, on a virtual array whose defects we know exactly. That is in fact the
only way to find out whether a method recovers the right answer, since on a real
array the truth is unknown.

## 9. Metrics

See `benchmarks/metrics.md`: pointing error, gain, side lobe level, beam width,
number of measurements, calibration time, robustness to noise and to temperature,
stability over time.

## 10. Main unknowns

1. The measurement quality achievable in the available environment.
2. Whether phase can be measured, or only power.
3. The real magnitude of channel errors in a home built assembly.
4. How significant coupling actually is at the chosen spacing.
5. The minimum number of measurements for an acceptable calibration.
6. How long a calibration stays valid.

## 11. Experiments

See `experiments/plan.md`. As in the RF modelling project, the work runs on two
tracks: a simulation track that can start immediately, and a hardware track
constrained by lead times.

## 12. Smallest credible prototype

Two elements. With two channels you can already measure a phase shift, steer a
simple beam, observe the effect of a cable error and test a calibration. Going to
four elements adds no new question, it adds resolution.

Starting with two channels sharply reduces cost and risk, and reaches a measurable
result very quickly.

## 13. What comes next

See `ROADMAP.md`.

## 14. What can be shared

See `docs/shared-resources.md`. The link with the RF modelling project is strong:
instruments, calibration, automation, S parameter processing, connectors, board
fabrication. The link with the FPGA projects is real but conditional: it only
matters if digital beamforming is chosen.

## 15. What would make this project pointless

- If the measurement environment cannot separate a pattern from the room echoes, no
  conclusion about radiation is possible. Fallbacks: conducted channel by channel
  measurement, differential measurement, or moving the algorithmic work to an
  acoustic array.
- If channel errors turn out to be negligible there is nothing to calibrate. That is
  unlikely, but in that case we can introduce controlled errors deliberately, which
  is still a valid study.
- If component costs exceed the budget, the digital or acoustic route becomes the
  fallback.
- If the project turns into assembling a commercial kit it loses its content. The kit
  can be a reference, not an end.

## Out of scope

- Building a complete radar.
- Transmitting at high power or outside licence exempt bands.
- A large element count array.
- Multi user antenna processing.
