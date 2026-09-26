# Hardware and measurement means

- Status: in progress, the measurement environment is the critical point
- Last reviewed: 2026-09-26

---

## 1. What decides this project

The main constraint here is neither budget nor components, it is **the ability to
measure a radiation pattern in an ordinary environment**.

Three questions, in this order:

1. Can we measure received power repeatably?
2. Can we measure it at several angles, with accurate positioning?
3. Are the room reflections weak enough not to mask the phenomenon?

If the answer to the third is no, the project has to change strategy, and it is
better to know that immediately.

## 2. Available hardware

> **Largely answered on 2026-09-20.** A Rohde and Schwarz ZVL was observed on the
> bench: 50 ohm, 9 kHz to 3 GHz, N female ports, transmission and complex formats
> available, source up to 0 dBm, USB present. That covers the working frequency and
> the measurements the calibration architecture needs. The instrument assignment for
> every Rev A task is in `docs/hardware/measurement-bench.md`, the readings are in
> `results/EXP-004/`, and what remains outstanding is listed there.
>
> Two cautions carried forward. The exact model and serial have not been read, so no
> reading has yet been checked against a datasheet. And the instruments documented in
> the laboratory inventory, which do not include this one, have **not** been confirmed
> to be physically present; they are treated as conditional cross checks only.
>
> Quantities below are what the first planning assumed. Only the rows marked observed
> or confirmed have evidence behind them today. Purchases are staged by decision 0006.

| Item | Quantity | Role here | Status |
| --- | --- | --- | --- |
| Vector network analyser | 1, in the school laboratory | channel measurement, coupling between elements, complex per element labels. Every task using it is `SCHOOL-BENCH`, `docs/runbooks/register.md` | **observed 2026-09-20**: Rohde and Schwarz ZVL, 9 kHz to 3 GHz, N female, complex formats, source to 0 dBm. Exact model, calibration kit, adapters and installed options still outstanding |
| Oscilloscope | 1, not confirmed | time domain measurement, coherence checks | **presence not confirmed**; model, bandwidth and sample rate unknown |
| Function generator | 1, not confirmed | source | **presence not confirmed**; model and maximum frequency unknown |
| Software defined radio | unknown | digital option, coherent channels | **presence unknown** |
| Terasic DE1-SoC | 3 | **the Rev A controller**, decision 0005: beam state application, sequencing, triggering and timestamps in fabric; orchestration, storage and inference on the processor. One of the three is enough | confirmed; expansion header current limit to verify |
| Digilent Zybo | 1 | only if digital beamforming is chosen, which it is not for Rev A | confirmed |
| STM32G0 Nucleo | 2 | **no longer the array controller**, decision 0005. Still the positioner controller | exact variant to record |
| ESP32 | 3 | remote telemetry for long unattended runs | exact variant to record |
| Gaming PC | 1 | optimisation, simulation sweeps | model to record |
| Stepper motor and driver | 0 | rotating the array for pattern measurement | **to acquire, see the bill of materials** |
| Absorbers | 0 | reducing reflections | **to acquire, or work around** |

The angular positioner is easy to underestimate. Measuring a pattern means rotating
the array or the probe in regular steps, dozens of times, repeatably. Doing it by
hand is fine for a few points, not for a full pattern, and the operator leaning over
the setup changes the measurement.

Building a simple positioner from a stepper motor and a microcontroller we already
own is an accessible and very useful sub-project. It would serve the RF modelling
project as well.

## 3. Available software, and what it changes

| Tool | Role | Consequence for this project |
| --- | --- | --- |
| 3D electromagnetic simulator (HFSS) | full wave simulation of the array | **can produce a physically grounded coupling matrix, rather than an invented one**. HFSS Student locally, within its documented limits, bibliography V7; the full licence at school, only for a model that exceeds them |
| Electromagnetic scripting (PyAEDT) | automating the above | makes geometry sweeps realistic |
| Circuit simulator (ADS) | feed network, phase shifters, matching | designs the distribution network before fabrication. **At school only, and optional**: scikit-rf's transmission line media give a local circuit route, `docs/runbooks/README.md` |
| S parameter library (scikit-rf) | measurement processing, de-embedding | **the shared radio frequency data layer**, pinned in `requirements.txt` and wrapped by `tools/rfkit`. Every S parameter from the solver, the circuit simulator and the analyser enters the project through it. See `docs/architecture/rf-data-layer.md` |
| MATLAB | array processing, optimisation | cross check on the algorithms |

The first row matters more than it looks. The project's simulator needs a coupling
model, and there were two options: invent a plausible one, or simulate the real
structure. Having a full wave simulator means the injected coupling can come from
physics rather than from a guess. That makes the simulation study substantially more
credible, and it is a genuine advantage over most amateur array projects.

## 4. The reflection problem

In an ordinary room the received signal is the sum of the direct path and several
echoes. The effect can reach several decibels, the same order as what we are
measuring.

Mitigations, cheapest first:

| Means | Expected effect | Cost |
| --- | --- | --- |
| Move the setup away from walls and floor | moderate | none |
| Differential measurement, array driven and not driven | good on stable echoes | none |
| Averaging over several positions | moderate | none, but slow |
| Time domain gating, if the instrument supports it | very good, it separates the direct path from later echoes | none if the function exists |
| Absorbers on the main surfaces | good | moderate |
| Anechoic chamber | excellent | out of reach |

The time domain gating row should be checked first. Some network analysers can
transform to the time domain and isolate the direct path from later reflections. If
that function is available it solves much of the problem for nothing.

## 5. The acoustic route

If the RF measurement environment turns out to be poor, an ultrasonic array removes
almost all of these problems.

| Aspect | RF array at 2.4 GHz | Acoustic array at 40 kHz |
| --- | --- | --- |
| Wavelength | 12.5 cm | about 8.6 mm |
| Half wavelength spacing | 6.25 cm | about 4.3 mm |
| Cost per element | moderate to high | very low |
| Phase shift generation | dedicated component or digital | directly digital, the frequency is low |
| Measurement | delicate | a microphone is enough |
| Reflections | hard to control | easier, absorbing materials are common |
| Subject realism | direct | an analogy, and it has to be explained |

The wavelength gap is the interesting complication: at 40 kHz elements would need to
sit a few millimetres apart, which is mechanically awkward with standard
transducers. So we would have to accept spacing greater than half a wavelength, and
therefore grating lobes. That is a real constraint, and it could itself become a
study subject.

An alternative is to move down into the audible range, where loudspeakers are easier
to space correctly, at the cost of a physically larger array.

These points have to be costed before choosing this route. It is promising but not
free.

## 6. What is missing

| Need | Workaround | Cost if bought |
| --- | --- | --- |
| Angular positioner | manual measurement at a few points | low, and buildable from parts |
| Absorbers | distance, time gating, differential measurement | moderate |
| Commanded phase shifters | switched line phase shifting, or the digital route | to cost, see the bill of materials |
| Coherent receive channels | stay analogue | high |
| Identical antennas | fabricate on a printed circuit board | low in a small batch |

## 7. Safety and regulation

- Very low power, no hazard.
- Frequencies chosen inside licence exempt bands.
- Radiated measurements stay local and at very low power.
- For the acoustic route, watch sound pressure levels if the design moves into the
  audible range.
