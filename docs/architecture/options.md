# Candidate architectures

- Status: open, nothing chosen
- Last reviewed: 2026-08-21

---

## 1. The three ways to form a beam

| Approach | Principle | Hardware per channel | Flexibility | Cost |
| --- | --- | --- | --- | --- |
| Analogue | phase shifters and attenuators on the RF signal, one conversion chain | one phase shifter, one attenuator | one beam at a time | moderate |
| Digital | a full conversion chain per channel, everything done by computation | a converter and a transceiver | total, several simultaneous beams | high |
| Hybrid | analogue sub arrays combined digitally | intermediate | intermediate | intermediate |

Direct consequence for this project: **the FPGA only matters in the digital or
hybrid approaches.** In the analogue case a microcontroller is ample for driving
phase shifters. That has to be decided consciously rather than inherited.

## 2. Implementation options

### Option A: analogue array with commanded phase shifters

Dedicated components apply an adjustable phase shift per channel.

| Aspect | Assessment |
| --- | --- |
| Electronic complexity | medium |
| Cost | depends heavily on the components, to be costed |
| Realism | this is how real systems are built |
| Calibration problem | well posed, and it is the subject |
| Role of the FPGA | none, a microcontroller is enough |

### Option B: digital multi channel array

Each channel has its own conversion chain, beamforming is done by computation.

| Aspect | Assessment |
| --- | --- |
| Complexity | high, the channels have to be kept coherent |
| Cost | high |
| Flexibility | maximal |
| Calibration problem | still present, and richer |
| Role of the FPGA | central, including for synchronisation |

A specific and interesting difficulty: channel coherence. Two separate receivers
each have their own oscillator, and their phase difference drifts. You need either a
shared clock or a reference channel. That is a genuine engineering problem, and it
connects directly to the synchronisation work in the latency project in this lab.

### Option C: switched line phase shifting

Select between different line lengths to create discrete phase steps, for example in
90 degree increments.

| Aspect | Assessment |
| --- | --- |
| Complexity | low |
| Cost | low |
| Accuracy | limited by phase quantisation |
| Teaching value | high, everything is visible and understandable |
| Limit | quantisation caps pointing accuracy |

Phase quantisation is a subject in itself: with 90 degree steps the worst case error
is 45 degrees, which degrades the pattern significantly. Studying that effect is
instructive and cheap.

### Option D: acoustic array

Move the whole problem to ultrasound, around 40 kHz.

| Aspect | Assessment |
| --- | --- |
| Cost | very low |
| Electronic complexity | low, phase shifting is done digitally at low frequency |
| Measurement | easy, with a microphone and a mechanical scan |
| Physics | identical in principle, wavelength about 8.6 mm |
| Limit | these are not electromagnetic waves, and that has to be said clearly |

This is not a gimmick. The entire algorithmic side, calibration, optimisation and
pattern measurement, is identical. It would produce complete, validated results very
quickly, and the method could then be carried over to an RF array.

Its drawback is presentational: an antenna array project that uses no antennas needs
an explanation. That explanation is easy to give if the results are good.

### Option E: commercial educational kit

A phased array already designed, documented and working.

| Aspect | Assessment |
| --- | --- |
| Cost | to check, probably significant |
| Time saved | considerable |
| Design learning | low |
| Value | lets you focus entirely on calibration and algorithms |

Worth considering honestly: if the main goal is studying calibration, starting from
an array that already works is not cheating, it is a scope choice. The risk is
ending up simply following a tutorial.

---

## 3. Comparison matrix

| Option | Cost | Lead time | Measurement difficulty | Richness of the calibration problem | Role of the FPGA | Risk |
| --- | --- | --- | --- | --- | --- | --- |
| A analogue | medium | medium | high | good | none | medium |
| B digital | high | long | high | excellent | central | high |
| C switched line | low | short | high | good, with quantisation | none | low |
| D acoustic | very low | very short | low | good | possible but unnecessary | very low |
| E commercial kit | to cost | short | medium | good | none | low |

**Suggested sequence, to discuss**: start with D to validate the calibration
algorithms under good measurement conditions, then move to A or C on two channels,
then extend. Option B only makes sense if digital beamforming becomes an explicit
goal.

That sequence has the same property as the one in the RF modelling project: every
step produces a usable result even if the next one never happens.

---

## 4. Antenna options

| Type | Fabrication | Bandwidth | Note |
| --- | --- | --- | --- |
| Printed antenna on a board | ordered | narrow | easy to reproduce identically, which is what matters for an array |
| Wire antenna | hand made | medium | element to element variation, which is exactly what we are studying |
| Commercial antenna | purchased | model dependent | decent reproducibility, cost per element |

Worth noting: reproducibility between elements matters more than the performance of
any single element. An array of four mediocre but identical antennas calibrates
better than four good but different ones.

---

## 5. Decisions to make later

| Decision | What is missing | Consequence |
| --- | --- | --- |
| Kind of wave, radio frequency or acoustic | evaluation of the available measurement means | everything else |
| Working frequency | instrument audit | dimensions, cost, measurement |
| Element count | budget and complexity | beam resolution |
| Phase shifting method | component cost | accuracy and the role of the FPGA |
| Analogue or digital | the project's main goal | cost and complexity |
| Pattern measurement method | available environment | credibility of every result |
