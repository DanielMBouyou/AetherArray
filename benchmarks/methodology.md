# Calibration method comparison methodology

- Status: in progress
- Last reviewed: 2026-08-21

---

## 1. The underlying problem

On a real array you do not know the truth. So you can tell whether a calibration
improved the result, but not whether it found the right parameters.

Hence a two stage arrangement:

| Stage | Object | What you can measure |
| --- | --- | --- |
| Simulation | virtual array with known injected defects | the estimation error, so the correctness of the method |
| Real | physical array | the improvement in the pattern, so practical effectiveness |

Both are needed. Simulation tells you whether the method is correct, the real array
tells you whether it survives noise and unmodelled imperfections.

## 2. The simulation bench

A simulator with injected defects is a cheap and very profitable tool. It lets every
method be compared before any hardware exists.

It must include:

| Element | Why |
| --- | --- |
| Per channel gain and phase errors, randomly drawn | the main defect |
| Coupling between neighbouring elements | to test methods that ignore it |
| Measurement noise, with an adjustable level | to test robustness |
| Command quantisation | if discrete step phase shifters are used |
| Slow drift | to test how long a calibration stays valid |

The key point is that the defects are **known**, so the estimation error is exactly
measurable. That is impossible on a real array.

One improvement over a naive simulator: the coupling model can come from a full wave
electromagnetic simulation of the actual planned geometry rather than from an
invented matrix. That makes the simulation study considerably more credible, and it
is available here.

## 3. Comparison protocol

For each calibration method:

1. Fix a defect draw, identical across methods.
2. Run the method, counting the measurements it consumes.
3. Record the estimation error in simulation, or the pattern quality on the real
   array.
4. Repeat across several defect draws and several noise levels.
5. Plot quality achieved against measurements consumed.

The curve in step 5 is the project's main result. It answers the real question: how
many measurements are needed, and what do you gain by taking more.

## 4. Measurements are the counted resource

Unlike the other projects in this lab, the scarce resource here is not compute time
but the **number of physical measurements**. A measurement means a mechanical move,
a settling time, and a noisy acquisition.

That is what makes Bayesian optimisation relevant: it is built for situations where
each evaluation is expensive.

So every method is characterised by at least two numbers: the quality reached, and
the number of measurements it took to reach it.

## 5. Real measurement protocol

| Step | Content | Why |
| --- | --- | --- |
| 1 | Check the setup, record cable lengths | cables are part of the system |
| 2 | Reference measurement on a single channel | detects global drift |
| 3 | Measure the uncalibrated pattern | the starting point |
| 4 | Apply the calibration method | counting the measurements |
| 5 | Measure the calibrated pattern | the result |
| 6 | Reference measurement again | detects drift during the campaign |
| 7 | Repeat a few hours later | measures how long the calibration lasts |

Step 7 produces the most original result and costs only patience.

## 6. Precautions specific to this project

| Precaution | Reason |
| --- | --- |
| Do not touch the setup between compared measurements | a retightened connector changes everything |
| Record ambient temperature | it explains part of the drift |
| Keep the operator away during the measurement | a human body reflects and absorbs |
| Repeat each measurement point | to estimate the noise |
| Measure a known case at the start and the end | to detect bench drift |

The third is not a joke: at these wavelengths a person standing next to the setup
changes the pattern measurably.

## 7. What gets compared

| Configuration | Role |
| --- | --- |
| Ideal simulation | what theory predicts |
| Real, uncalibrated | the starting point, often spectacularly bad |
| Channel by channel calibration | the basic method |
| Phase rotation calibration | classical, needs no phase measurement |
| Regularised inversion | the full method |
| Direct optimisation | without estimating the matrix |
| Bayesian optimisation | to cut the number of measurements |
| Possible learned method | if it adds anything |

## 8. What we will not do

- No comparison without counting measurements.
- No conclusion from a single defect draw.
- No pattern published without the measurement conditions and the environment.
- No simulation result presented as a measurement.
