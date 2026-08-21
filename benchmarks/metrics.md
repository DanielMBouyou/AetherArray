# Metrics

- Status: in progress
- Last reviewed: 2026-08-21

---

## 1. Pattern metrics

| Metric | Definition | Unit | Note |
| --- | --- | --- | --- |
| Pointing error | difference between the requested direction and the observed maximum | degrees | the most legible metric |
| Gain in the wanted direction | received power relative to one element | dB | measures how well the recombination works |
| Side lobe level | ratio of the highest side lobe to the main lobe | dB | often more degraded than the gain |
| Half power beam width | angle between the -3 dB points | degrees | should match theory |
| Deviation from the target pattern | overall difference between achieved and wanted patterns | dB | a synthesis metric |

Pointing error is the one to lead with, because it is immediately understandable:
the beam does not go where you asked, and you can show it on a plot.

## 2. Estimation metrics, simulation only

| Metric | Definition | Use |
| --- | --- | --- |
| Error on the estimated phases | difference between estimated and injected phases | measures whether the method is correct |
| Error on the estimated gains | same for amplitudes | same |
| Residual matrix error | norm of the difference between estimated and true matrix | overall view |
| Condition number | measure of how stable the inversion is | predicts noise sensitivity |

These are only available in simulation, since they require knowing the truth. That is
exactly why the simulation bench is indispensable.

## 3. Cost metrics

| Metric | Unit | Why |
| --- | --- | --- |
| Number of physical measurements | count | the scarce resource in this project |
| Calibration time | minutes | includes mechanical movement |
| Compute time | seconds | usually negligible against the rest |
| Number of angular positions needed | count | drives the total time |

The ratio between the first and third rows is striking: a measurement takes seconds
or minutes, the computation behind it takes milliseconds. Optimising the computation
is pointless, optimising the number of measurements is worth a great deal. That
imbalance shapes the whole project.

## 4. Robustness metrics

| Metric | Definition | How to measure it |
| --- | --- | --- |
| Noise sensitivity | degradation as measurement noise rises | sweep in simulation, repeated measurements on the real array |
| Stability over time | pattern degradation after a few hours with no recalibration | repeated measurements |
| Thermal sensitivity | variation with temperature | measurements at several temperatures |
| Sensitivity to reconnection | effect of disconnecting and reconnecting cables | repeated measurements after handling |

The last row measures something important: if simply unplugging and replugging a
cable invalidates the calibration, that completely changes how the system could be
used.

## 5. Standard results table

| Method | Measurements | Pointing error | Gain | Side lobes | Beam width | Still valid after a few hours |
| --- | --- | --- | --- | --- | --- | --- |
| uncalibrated | 0 | to measure | to measure | to measure | to measure | not applicable |
| channel by channel | to measure | to measure | to measure | to measure | to measure | to measure |
| phase rotation | to measure | to measure | to measure | to measure | to measure | to measure |
| regularised inversion | to measure | to measure | to measure | to measure | to measure | to measure |
| Bayesian optimisation | to measure | to measure | to measure | to measure | to measure | to measure |

The first row is the control. It is what tells you how much calibration actually
buys, and it is the easiest row to fill in.

## 6. What we will not do

- No pattern metric quoted without the measurement conditions.
- No method comparison without the measurements consumed.
- No conclusion from a gap smaller than the repeated measurement noise.
- No simulation result presented without its label.
