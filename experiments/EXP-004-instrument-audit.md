# EXP-004: instrument audit and the working frequency

- Status: running, five of nine observations recorded, O2, O4 and O5 all passing
- Date: 2026-09-19
- Estimated effort: 2 days originally, now about 30 minutes at the bench
- Results: `results/EXP-004/`

## Question

Which working frequency should Rev A use, and can the available network analyser
support the measurements the calibration architecture needs?

## Hypothesis

Written before the bench visit. The admissible band is 2400 to 2483.5 MHz with a
design centre of 2.44 GHz, and the analyser reaches it.

There is **no low frequency radio fallback**. That is a finding, not an omission, and
it is established in the regulatory section below: every sub-band between 863 and
870 MHz is limited either to a duty cycle of at most 10 per cent or to listen before
talk, and a swept analyser satisfies neither.

## Decision criterion

One observation decides it, and the rule is fixed here so that the bench visit closes
the question rather than reopening it.

| Observation O2, the analyser upper frequency | Decision |
| --- | --- |
| At or above 2500 MHz | **freeze $f_0 = 2.44$ GHz**, band 57a, 2400 to 2483.5 MHz, 10 mW equivalent isotropic radiated power, no duty cycle restriction. Conducted and radiated measurement are both available |
| Below 2500 MHz | **do not choose another radio band.** No licence exempt band below 2.4 GHz permits the continuous carrier a swept measurement needs. Reopen decision 0003 and choose between the two options in "If O2 falls short" below |

The second row is deliberately not a frequency. Picking one would mean picking a band
whose conditions this project cannot meet.

## Setup

Nothing is connected and nothing is powered. This is a reading exercise at the front
panel, plus a photograph of the rear label.

| Item | Reference | Setting | Note |
| --- | --- | --- | --- |
| Network analyser | unknown, to be recorded as O1 | as found | the subject of the audit |
| Oscilloscope | unknown | as found | recorded while there, not on the critical path |
| Signal generator | unknown | as found | same |
| Calibration kit | unknown | as found | O7 |

## Procedure

Nine observations. Each has an expected value, so an unexpected reading is visible as
soon as it is written down rather than at analysis time.

| N | Observation | Where to look | Expected value or acceptance criterion | What it decides |
| --- | --- | --- | --- | --- |
| O1 | Manufacturer, model, serial number | rear label, or the splash screen | any model recorded in full | identity, and which datasheet applies |
| O2 | Maximum sweep frequency | set the stop frequency field as high as it will accept | at or above 2500 MHz to take the preferred branch | **the whole decision, see above** |
| O3 | Minimum sweep frequency | set the start frequency field as low as it will accept | at or below 100 MHz | cable and connector characterisation headroom |
| O4 | Is a transmission measurement available | measurement or parameter menu | an S21 trace can be selected; forward only is sufficient | gate G1, and whether per element complex labels are possible |
| O5 | Is complex data available | format menu | at least one of Smith, polar, or real and imaginary is present, not only SWR and magnitude | gate G1. Magnitude only forces the power only branch |
| O6 | Source power setting and range | stimulus or power menu | a level available inside $-25$ to $+8$ dBm. **Record the value that will actually be used**, because the upper end is a regulatory ceiling, not a preference | radiated measurement procedure and the e.i.r.p. check, see "Analysis" |
| O7 | Calibration kit present, and its connector type | physical inspection of the case and accessories | a short, open and load, for SMA or for N with adapters | whether a calibrated measurement is possible at all |
| O8 | Time domain or gating function | analysis, transform or measurement menu | presence recorded. **Absence is acceptable** and is not a gate | uncertainty I2, and the echo strategy for EXP-005 |
| O9 | Remote interface | rear panel, then connect to the computer and see whether it enumerates | a USB or LAN interface that the computer recognises | automation for EXP-014, not a gate for Rev A |

Record each reading in `results/EXP-004/` with the date, next to the expected value.

## Error sources identified before measuring

- A front panel that accepts a stop frequency above the specified range without
  warning. O2 is confirmed against the model datasheet found from O1, not against the
  field alone.
- A model number on a sticker that belongs to the case rather than to the instrument.
- An option that is present in a menu but not licensed, which appears as a greyed
  entry or an error on use. O8 is the likely candidate.
- Confusing a scalar antenna analyser with a vector instrument. O5 separates them.

## Independent check

O1 gives a model. The model gives a datasheet. Every reading from O2 to O8 is then
checked against that datasheet rather than trusted from the panel. Where the two
disagree, the datasheet wins for design purposes and the disagreement is recorded.

## Raw results

In `results/EXP-004/`.

## Analysis

The part of the analysis that does not need the bench has been done, so that the visit
is a lookup rather than a study.

### Admissible interval from the hardware already chosen

| Constraint | Value | Source | Effect |
| --- | --- | --- | --- |
| PE4259-63 operating range | 10 MHz to 3000 MHz | bibliography V1 | **hard upper bound of 3.0 GHz** |
| AD8318 range and accuracy | 1 MHz to 8 GHz, $\pm 1$ dB over 55 dB below 5.8 GHz | bibliography V6 | not binding anywhere in the interval |
| Grating lobe condition | $d \leq \lambda/2$ | `docs/mathematics/formulation.md` | sets spacing, therefore array size |

### The regulatory constraint, from the primary source

Commission Implementing Decision (EU) 2022/180, amending Decision 2006/771/EC, annex,
non-specific short range devices. Bibliography R1, consulted 2026-09-19. Rows quoted
as written.

| Band | Limits | Power | Spectrum access and duty cycle |
| --- | --- | --- | --- |
| 46a | 863 to 865 MHz | 25 mW e.r.p. | mitigation techniques apply, or a duty cycle limit of 0.1 per cent |
| 47 | 865 to 868 MHz | 25 mW e.r.p. | mitigation techniques apply, or a duty cycle limit of 1 per cent |
| 48 | 868 to 868.6 MHz | 25 mW e.r.p. | mitigation techniques apply, or a duty cycle limit of 1 per cent |
| 50 | 868.7 to 869.2 MHz | 25 mW e.r.p. | mitigation techniques apply, or a duty cycle limit of 0.1 per cent |
| 54 | 869.4 to 869.65 MHz | 500 mW e.r.p. | mitigation techniques apply, or a duty cycle limit of 10 per cent |
| 56b | 869.7 to 870 MHz | 25 mW e.r.p. | mitigation techniques apply, or a duty cycle limit of 1 per cent |
| **57a** | **2400 to 2483.5 MHz** | **10 mW e.i.r.p.** | **none stated** |

Two consequences, and they decide the experiment.

**The 863 to 870 MHz band has no usable frequency for this work.** Every sub-band
requires either a spectrum access mitigation technique, meaning listen before talk with
adaptive frequency agility, or a duty cycle capped at 10 per cent in the most generous
case and 1 per cent in most. A network analyser sweeping a band emits an essentially
continuous carrier and offers neither. The generic phrase "the 868 MHz band" that an
earlier draft of this document used does not correspond to any frequency this project
could legally radiate on. It has been removed rather than narrowed.

**Band 57a carries no duty cycle restriction at all**, so a continuous carrier is
permitted provided the radiated level stays at or below 10 mW equivalent isotropic
radiated power. That is the condition the link budget below is checked against.

Two limits of this evidence, recorded rather than glossed. The decision is the European
harmonisation instrument, and the national table of allocations may be more
restrictive; that should be checked once before any radiated measurement. And nothing
here is about an amateur licence, which if held would open other allocations under
different conditions. Neither changes the conclusion for an unlicensed bench.

### Conducted measurement is not affected

Worth stating plainly, because it is what keeps the project alive in the fallback case.
Regulation constrains radiation. The per element transfer measurements, the element to
element coupling measurements and the sum port detector readings are all conducted
through cables and radiate nothing of consequence. Only pattern measurement radiates.

Array geometry for four elements at half wavelength spacing, where the aperture is
taken as the span of the element centres, $D = 3d = 1.5\lambda$, and the far field
distance as $2D^{2}/\lambda = 4.5\lambda$:

| Candidate | $\lambda$ | Spacing | Aperture | Far field distance | Status |
| --- | --- | --- | --- | --- | --- |
| 433 MHz | 692 mm | 346 mm | 1.04 m | 3.11 m | eliminated twice over: a one metre aperture needing a three metre range is not a bench experiment, and the band is duty cycle limited |
| 869 MHz | 345 mm | 173 mm | 518 mm | 1.55 m | **eliminated by the regulatory table**: no sub-band permits a continuous carrier |
| **2.44 GHz** | **122.9 mm** | **61.4 mm** | **184 mm** | **0.55 m** | **the only surviving candidate** |

### Why 2.44 GHz is the answer rather than merely the preference

It is the only licence exempt band below the 3.0 GHz component ceiling that permits a
continuous radiated carrier. That alone decides it. The geometry then happens to
favour it as well: the project's own documents name the measurement environment as the
thing most likely to sink it, far field distance is the dominant lever on that risk,
and 0.55 m is the shortest of the three. Absorbing material also works better at the
shorter wavelength, since its thickness scales with $\lambda$.

### What 2.44 GHz costs, quantified

Switch isolation falls with frequency, and it sets the floor of one measurement.

**What is sourced, and what is not.** The manufacturer states two isolation figures,
30 dB at 1000 MHz and 20 dB at 2000 MHz, and two insertion loss figures, 0.35 dB at
1000 MHz and 0.5 dB at 2000 MHz. These are **typical** values quoted at spot
frequencies in the product description, bibliography V1. **No guaranteed minimum
isolation has been obtained at any frequency, and no value of any kind has been
obtained at 2.44 GHz.** The datasheet carries the curve, but the file is a scanned
image and could not be read here.

An earlier draft of this document extrapolated to about 18 dB at 2.44 GHz. That number
has been removed. It was an interpolation between two typical spot values presented as
if it were a specification, which is exactly the habit `CONVENTIONS.md` forbids.

The analysis below is therefore parametric in the isolation $I$, so that reading the
curve once fills it in without redoing anything.

When one channel is enabled and the other three are terminated, each disabled channel
still leaks. Three channels leaking at isolation $I$, adding with random relative
phase, give a residual amplitude relative to the wanted channel of

```math
r_{\text{rms}} = \sqrt{3}\,\cdot\,10^{-I/20},
\qquad
r_{\text{worst}} = 3\,\cdot\,10^{-I/20}
```

| Symbol | Meaning | Unit |
| --- | --- | --- |
| $I$ | switch isolation at the working frequency | dB |
| $r_{\text{rms}}$ | residual for random relative phase, the typical case | dimensionless ratio |
| $r_{\text{worst}}$ | residual when the three leakages add coherently | dimensionless ratio |

| $I$ | $r_{\text{rms}}$ | Amplitude error | Phase error | $r_{\text{worst}}$ |
| --- | --- | --- | --- | --- |
| 14 dB | -9.2 dB | 35 per cent | 20 degrees | -4.5 dB |
| 16 dB | -11.2 dB | 27 per cent | 16 degrees | -6.5 dB |
| 18 dB | -13.2 dB | 22 per cent | 13 degrees | -8.5 dB |
| 20 dB | -15.2 dB | 17 per cent | 10 degrees | -10.5 dB |
| 25 dB | -20.2 dB | 10 per cent | 6 degrees | -15.5 dB |
| 30 dB | -25.2 dB | 5 per cent | 3 degrees | -20.5 dB |

Two rows of that table are anchored to sourced values, 30 dB at 1000 MHz and 20 dB at
2000 MHz, and the rest are there to be selected from once the curve is read. The
acceptance criterion for the B2 baseline is written against $r_{\text{worst}}$, not
against $r_{\text{rms}}$.

Whatever the value turns out to be, the structural point does not depend on it: this
degrades the element by element baseline B2 taken **at the sum port**, and does not
degrade the per element measurement taken at the element connectors, because that path
does not pass through the other channels. Requirement R1 protects the labels the
learning track depends on, and the cost falls on one baseline rather than on the
central experiment.

This degrades the element by element baseline B2 when it is taken at the sum port. It
does **not** degrade the per element complex measurement taken at the element
connectors, because that path does not pass through the other channels. Requirement R1
therefore protects the labels that the learning track depends on, and the cost of
2.44 GHz falls on one baseline rather than on the central experiment.

### Source power has an upper bound, and it comes from the regulation

Corrected on review. An earlier draft said source power was not a constraint, which was
right about sensitivity and wrong about compliance. There is a ceiling.

At 2.44 GHz with a transmit probe of about 2 dBi, an array gain of about 8 dBi, a chain
loss of about 4 dB, and free space loss of 35.8 dB at 0.6 m, which is just beyond the
0.55 m far field distance, the level at the sum port is the source level less 29.8 dB.

| Source level $P_t$ | Radiated e.i.r.p. | Level at the sum port | Verdict |
| --- | --- | --- | --- |
| -25 dBm | -23 dBm | -54.8 dBm | near the bottom of the useful detector range |
| -13 dBm | -11 dBm | -42.8 dBm | comfortable, and typical of a fixed output instrument |
| 0 dBm | +2 dBm | -29.8 dBm | comfortable |
| **+8 dBm** | **+10 dBm** | -21.8 dBm | **at the band 57a limit of 10 mW e.i.r.p.** |
| +10 dBm | +12 dBm | -19.8 dBm | **exceeds the limit, not permitted** |

So the usable window is roughly $-25$ dBm to $+8$ dBm at the source with a 2 dBi probe,
and the upper end scales down by whatever gain the probe has above 2 dBi. Any ordinary
instrument sits inside it, including a fixed output around $-13$ dBm.

Observation O6 is therefore recorded for a reason: it is the number the radiated
measurement procedure must be written against, and it must not be raised to the
instrument maximum without recomputing the e.i.r.p.

### What the answer does not change

Both surviving candidates sit inside the PE4259-63 range, and the AD8318 covers both
with margin. **The schematic and the bill of materials committed for Rev A are valid
under either outcome.** Only the printed line lengths and the antenna geometry depend
on the answer, and both are layout parameters. That is the separation decision 0003
was built on, and this audit does not disturb it.

### If O2 falls short

If the analyser stops below 2500 MHz there is no compliant radiated radio option at
this array scale, so the question becomes which capability to give up. Two options,
both of which reopen the frequency in decision 0003 while leaving its topology,
part choices and control interface untouched.

| Option | Keeps | Loses |
| --- | --- | --- |
| Conducted only, at a frequency inside the analyser range | the per element transfer measurements, the coupling measurements, the sum port detector path, and therefore the whole calibration and learning programme | radiated pattern measurement, so EXP-007 becomes a conducted demonstration and EXP-009 loses its pattern evidence |
| The acoustic route, `docs/architecture/options.md` option D | everything, including pattern measurement, with no spectrum regulation at all | the radio frequency content, which has to be argued for rather than assumed |

The first option is stronger than it looks. Most of this project's measurement
programme is conducted, and the label mechanism that supervises the learned drift prior
is conducted end to end.

### If O4 or O5 fails

If no transmission measurement or no complex format is available, gate G1 fails. The
consequences are larger than the frequency question: the orthogonal coding baseline B5
becomes unavailable, and the per element complex label that supervises the learned
drift prior has to be obtained another way or abandoned. The rotating element field
vector method and the on board detector still work, so the project continues, but
decision 0002 needs revisiting. Record this outcome loudly if it occurs.

## Conclusion

**Not yet available, but much closer.** Update of 2026-09-20: a Rohde and Schwarz ZVL
was observed on the bench, and the three observations that decide the frequency all
pass. O2 is 3 GHz against a criterion of 2500 MHz, O4 gives a transmission
measurement, and O5 gives complex formats.

The frequency is still not frozen, for one reason only: **O1 has not been read.** The
procedure above requires every reading to be checked against the datasheet of the exact
model, and "a ZVL" does not identify a datasheet. The observed behaviour matches the
ZVL3, the 3 GHz member of the family, but that is an inference from behaviour and the
rear label settles it in seconds.

The remaining observations and the instrument assignment for every Rev A measurement
are in `docs/hardware/measurement-bench.md`. The practical risk has moved: it is no
longer the frequency, it is whether a calibration kit and the adapters to reach an SMA
reference plane exist at all, which is observation O7.

What is established is that no local evidence can identify the instrument. The search
is recorded in `results/EXP-004/`, and it was exhaustive enough to be worth not
repeating.

What is also established is that the decision is now a single binary reading. Whatever
O2 returns, the rule above gives the answer without further analysis.

What changed on review, 2026-09-19, is that the fallback disappeared. The regulatory
table above shows that the band an earlier draft named as the fallback cannot carry a
continuous carrier under any of its sub-band conditions. There is one admissible radio
frequency for this array, 2.44 GHz, and if the analyser cannot reach it the answer is a
change of measurement mode or of medium, not a change of frequency.

## Follow-up

- Record the readings in `results/EXP-004/`.
- Read the PE4259-63 isolation curve at 2.44 GHz from the datasheet, which needs a
  human with the file open because it is a scanned image, and note whether the value is
  typical or guaranteed. Then select the matching row of the parametric table.
- Check the national table of allocations once against band 57a before any radiated
  measurement.
- Write decision 0004 fixing the working frequency, citing O1 and O2.
- Then, and only then, compute the physical line lengths in
  `hardware/rev-a/layout-constraints.md`.
- EXP-005 follows, and O8 shapes its echo strategy.
