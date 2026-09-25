# EXP-005: the repeatability floor, and whether the control path disturbs it

- Status: planned, Phase A executable now, Phase B gated on hardware not yet bought
- Date: 2026-09-25
- Estimated effort: Phase A about two days including the test harness
- Results: `results/EXP-005/`

This experiment decides two requirements before anything is drawn or bought:
requirement R9, the deterministic quiet window, and open item H3, the converter on the
radio frequency board. Both were adopted in decision 0005 on reasoning rather than
measurement, and both were recorded there as precautions rather than findings.

**The decision rules in section 7 are fixed before any measurement is taken.** The
commit that introduces this file is the timestamp. A rule may be found inadequate, in
which case that is recorded as a failure of the protocol and the experiment is redone,
but a rule is not retuned after seeing a number.

---

## 1. What is actually being asked

Three different things get called noise, and the experiment exists to separate them.

| Quantity | What it is | Why it matters here |
| --- | --- | --- |
| Ordinary measurement noise | random scatter, sample to sample | sets the floor; averaging reduces it |
| Environmental drift | slow movement of the mean with temperature, time, handling | slow enough to be tracked, and it is the subject of EXP-010 |
| **State correlated error** | a shift in the reading that depends on **which beam state was commanded** | **the dangerous one.** It does not look like noise. It looks like a calibration coefficient, so the calibration faithfully absorbs it and reports a hardware property that does not exist |

Only the third justifies the quiet window and the local converter. The first two would
be present with any controller.

### Hypotheses

| | Statement |
| --- | --- |
| **H-A** | Digital traffic on the control cable during acquisition produces a state correlated error in the digitised detector voltage. |
| **H-B** | Holding the control lines and the temperature bus static from the strobe to the end of conversion removes that error. |
| **H-C** | Carrying the analogue signal along the control cable to a converter at the controller produces more error than converting it locally. |

H-A and H-B decide R9. H-C decides H3. The null form of each is the one to beat: no
measurable effect.

---

## 2. Why the detector is not needed for Phase A

The detector is not yet bought, and Phase A does not wait for it.

What H-A, H-B and H-C concern is the **acquisition path**, not the detector. The
detector is only a source of a slowly varying voltage in the 0.4 V to 2.2 V range. A
stable direct voltage substitutes for it exactly, and is better for this purpose,
because its true value is known to be constant: any state correlated change in the
reading is then unambiguously the path, not the source.

Phase B, which needs the detector, answers the original question of this experiment:
whether received power can be measured repeatably in the available environment. That is
a different question and is gated separately.

---

## 3. Apparatus, from hardware already owned

Nothing here is bought. The local converter path is realised with a **second DE1-SoC**,
of which three are owned.

That choice matters methodologically: both paths then use the **same converter type,
the same reference and the same harness**, so a difference between them cannot be a
difference between converters. The only thing that differs is the cable and the
proximity to switching traffic, which is the variable under test.

| Item | Role | Status |
| --- | --- | --- |
| DE1-SoC, board 1, at the controller end | drives the cable, converts the far path | owned |
| DE1-SoC, board 2, at the source end | converts the local path with a short lead | owned |
| Ribbon cable, 40 way, 0.3 m to 1 m | the path under test | **confirm one is available before starting** |
| Direct voltage source meeting S1 below | stands in for the detector | **choose and confirm, see S1** |
| Two resistors for a divider, if needed | sets the level | ordinary parts |
| Room thermometer | temperature log | **confirm available** |

### S1, the source specification

| Property | Requirement | Why |
| --- | --- | --- |
| Output level | between 0.4 V and 2.2 V, near 1.2 V preferred | the range the detector will occupy |
| Stability | better than 0.2 mV over one interleave cycle, about 60 s | must be well below the 0.5 mV effect being looked for |
| Source impedance | 100 ohm or less; up to 1 kohm is acceptable if the sample rate is reduced to 50 ksps or below | a successive approximation converter kicks charge back into the source, and a stiff source settles it |
| Reference | its return tied to the ground at the source end | this is how the detector will be referenced |

Candidate realisations, in preference order. **The operator picks one and records which.**

| Candidate | Status | Note |
| --- | --- | --- |
| A cell and a resistive divider | ordinary parts | quiet and independent of both boards, which is the point |
| Function generator set to a direct offset with no waveform | owned, model unknown | confirm it can output direct voltage only, and check its stability against S1 |
| A converter output on a Nucleo | owned, variant unknown | confirm the variant has one |

**Do not use a rail of either DE1-SoC as the source.** That couples the source to the
very activity under test and would confound the result.

### Before starting, five things to confirm and record

These are the assumptions the protocol would otherwise leave implicit. Each is a lookup
or a five minute check, and each is recorded in `results/EXP-005/` section 0.

| | Confirm | Where |
| --- | --- | --- |
| B1 | Which header carries the converter's analogue inputs, which channel numbers, and whether any scaling or protection network sits in front of them | the board's user manual, bibliography T6 |
| B2 | Which converter example is used to read it, and its version | a vendor or published example exists for this board; record which one rather than describing it |
| B3 | That a ribbon of the intended length is available, and its length | inspection |
| B4 | That the chosen source meets S1, by measuring it | measure before use, not after |
| B5 | That a room thermometer is available | inspection |

**Absolute accuracy is not required anywhere in Phase A.** Both paths are the same
converter on the same board type, so any scaling, offset or reference error is common to
them and cancels in the comparison. Every decision rule in section 7 is a difference or
a spread, never an absolute level. This is why B1 matters for wiring and not for
accuracy.

---

## 4. Wiring

```
        source end                                  controller end
   ------------------                          ----------------------
   [ S1 source ]---+--- short lead ---> [ DE1-SoC 2 ADC in ]
                   |
                   +--- ribbon wire ------------> [ DE1-SoC 1 ADC in ]
                                    (analogue)
   [ ribbon far end ]  <=== 16 control + 1 strobe ===  [ DE1-SoC 1 GPIO ]
   open, header only        2 I2C-like lines
                            1 cross trigger  ========>  [ DE1-SoC 2 trigger in ]
                            ground wires, interleaved
```

The sixteen control lines terminate in the header at the far end and are otherwise
open. That approximates the real load, which is the high impedance input of a buffer,
to within the buffer's input capacitance. **Recorded as an approximation**: the real
board presents a few picofarad per line that this fixture does not.

The two boards share ground **only through the ribbon**, which is the case under test.
Condition C5 adds a strap to test the alternative.

---

## 5. Conditions

Four required, one optional. Every condition is run at the same source level and in
the same interleaved cycle.

| | Condition | Control lines | Temperature bus lines | Purpose |
| --- | --- | --- | --- | --- |
| C1 | static | held at one fixed pattern throughout | idle | the floor |
| C2 | active | toggling continuously, **including during conversion** | I2C-like traffic running during conversion | the condition the design forbids, measured to size what it forbids |
| C3 | quiet window | toggling between states, **static from strobe to end of conversion** | scheduled outside the window | the proposed design |
| C4 | bus only | static | I2C-like traffic during conversion | isolates the temperature bus contribution, which shares the same cable |
| C5 | quiet window plus ground strap | as C3 | as C3 | optional, informs open item H5 |

C4 exists because the temperature bus is easy to forget: it is two more switching lines
in the same cable, and scheduling a sensor read during a conversion would reintroduce
exactly what C3 removes.

### Beam state set

Sixteen distinct words, cycled in fixed order: the eight single bit patterns walking
through bits 0 to 7, then eight words drawn once from a fixed seed and written into the
protocol so every session uses the same set.

### Interleaving

Conditions are **interleaved, not blocked**: one cycle runs C1, C2, C3, C4, and C5 if
used, and the cycle repeats. Slow drift of the source or the room is then common to all
conditions and cancels in the contrast between them. Blocking the conditions would
confound drift with condition and is not acceptable.

---

## 6. Counts, sweeps and logging

| Parameter | Value | Reason |
| --- | --- | --- |
| Samples per state per condition per cycle, $m$ | 1000 | at 500 ksps this is 2 ms, and it reduces quantisation to well under the effect sought |
| States per cycle, $S$ | 16 | enough to estimate a between state variance |
| Cycles, $R$ | 20 | averages slow drift and gives a spread on every metric |
| Settling sweep | strobe to conversion delay over 1, 3, 10, 30, 100, 300 microseconds and 1, 3, 10 ms, in C3 | finds where the reading stops changing, which sets the sequencer's settling interval |
| Reconnection repetitions | at least 5 unplug and replug of the ribbon, at least 3 of the analogue leads | the reconnection metric, and uncertainty I14 |
| Session repetitions | at least 3 sessions on different days | separates within session from between session behaviour |
| Temperature | recorded at the start and end of every cycle | no board sensor exists yet, so this is a room reading, and the limitation is recorded |
| Time | elapsed time recorded with every cycle | drift is a function of it |

### Converter resolution and dither

The onboard converter is 12 bit over 4.096 V, so one step is 1.0 mV, which is
0.04 dB at the detector slope of $-25$ mV/dB. One step is larger than the effect being
looked for, and averaging only recovers resolution if the signal moves across at least
one step.

**Validity check before any averaging**: the raw codes in a burst must show at least two
adjacent distinct values. If they do not, the reading is stuck on one code, averaging is
meaningless, and dither must be added before the experiment proceeds.

---

## 7. Metrics and decision rules, fixed in advance

### 7.1 Metrics

For each path $p$, condition $c$ and cycle, from the raw codes:

| Metric | Definition |
| --- | --- |
| Mean | mean of all samples, in mV and in dB equivalent at $-25$ mV/dB |
| Within state spread | pooled standard deviation of samples inside a state, $\sigma_{\text{within}}$ |
| Between state spread | standard deviation of the per state means, $\sigma_{\text{between}}$ |
| **State correlated error** | see below |
| Reconnection shift | change in mean across an unplug and replug |
| Drift rate | slope of the mean against elapsed time, with temperature recorded alongside |

The state correlated error is the variance component that the within state noise does
not explain:

```math
e_{\text{state}} = \sqrt{\max\left(0,\; \sigma_{\text{between}}^{2} - \frac{\sigma_{\text{within}}^{2}}{m}\right)}
```

| Symbol | Meaning | Unit |
| --- | --- | --- |
| $\sigma_{\text{between}}$ | standard deviation of the per state means | mV |
| $\sigma_{\text{within}}$ | pooled standard deviation within a state | mV |
| $m$ | samples per state | count |
| $e_{\text{state}}$ | the part of the per state spread not explained by noise | mV |

Subtracting $\sigma_{\text{within}}^{2}/m$ matters: with 16 states and finite samples,
the per state means scatter even when nothing is state dependent, and reporting that
scatter as an effect would manufacture one.

### 7.2 Validity preconditions

No decision rule applies unless all four hold. If one fails, the setup is at fault and
is fixed before the experiment counts.

| | Precondition |
| --- | --- |
| V1 | Raw codes show at least two adjacent distinct values, see section 6 |
| V2 | $\sigma_{\text{within}}$ on the local path in C1 is at most 2 mV |
| V3 | Source drift within one cycle, from the first to the last C1 block, is at most 0.5 mV |
| V4 | The two paths agree at rest to within 3 mV, a gross error check on wiring and reference |

### 7.3 The threshold

**0.5 mV, which is 0.02 dB at the detector slope.** Chosen because it is about one
fortieth of the AD8318 stability figure over temperature and about one fifth of a
0.1 dB drift signal, so an acquisition path contributing less than this cannot dominate
what the drift experiment is trying to see.

### 7.4 Rules for R9, the quiet window

Evaluated on the far path, which is the one exposed to the cable.

| Observation | Outcome |
| --- | --- |
| $e_{\text{state}}$ in C2 at most 0.5 mV | **Demote R9.** Traffic during acquisition does not measurably matter, and the quiet window buys nothing |
| $e_{\text{state}}$ in C2 above 0.5 mV and at most 1.0 mV | **Keep R9 provisionally.** Borderline, and it costs nothing in parts. Record the number |
| $e_{\text{state}}$ in C2 above 1.0 mV, and in C3 at most 0.5 mV | **Keep R9, justified.** Traffic matters and the quiet window removes it |
| $e_{\text{state}}$ in C3 above 0.5 mV, whatever C2 shows | **Escalate.** The quiet window as specified does not fix it. R9 is insufficient and the path needs redesign: shielding, a differential analogue pair, or isolation. Decision 0005 reopens |
| $e_{\text{state}}$ in C4 above 0.5 mV | The temperature bus alone is a contributor, and scheduling sensor reads outside the window becomes mandatory rather than tidy |

### 7.5 Rules for H3, the converter on the radio frequency board

Evaluated in C3, because that is the condition the design actually operates in.

| Observation | Outcome |
| --- | --- |
| Far path $\sigma_{\text{within}}$ at most 1.2 times the local path, **and** far path $e_{\text{state}}$ at most 0.5 mV, **and** far path reconnection shift within 0.5 mV of the local path | **Demote H3.** Use the controller's own converter, and drop the four serial lines from the interface |
| Far path $\sigma_{\text{within}}$ above 2 times the local path, **or** far path $e_{\text{state}}$ above 1.0 mV | **Keep H3, justified by measurement** rather than by precaution |
| Anything between | **Keep H3 provisionally.** It is a few euro, and the asymmetry argued in decision 0005 still applies. Record the numbers |

### 7.6 What C5 decides

If C5 differs from C3 by more than 0.5 mV on any metric, the grounding arrangement
between the two boards is a live variable and open item H5 is upgraded from a layout
question to a measured requirement.

---

## 8. What Phase A needs built, and what it does not

The distinction the protocol depends on: this is a **test harness**, not the production
control path.

| Needed for Phase A | Not needed for Phase A |
| --- | --- |
| A converter read loop, the vendor example is sufficient | the production beam state register with read back |
| A pattern generator stepping the 16 lines through the state set | the sequencer entry list with repeat counts |
| A toggler producing bus like traffic on two lines | a real I2C master and real sensors |
| A gate that suppresses toggling between strobe and end of conversion | the timestamp counter with rollover handling |
| A cross trigger so both boards convert together | the processor bridge and the record schema |
| Capture of raw codes to memory, then dumped | storage, session metadata, inference |

**What needs no logic at all**: condition C1. The sixteen lines can be held at a fixed
pattern from the slide switches through a direct assignment, and the converter read with
the vendor example. C1 alone establishes V1, V2 and the floor, and is worth running
first as a shakedown.

**What needs the harness**: C2, C3, C4 and C5, because they require patterns and, for
C3, synchronisation between toggling and conversion.

No production RTL is written here, no part is selected for H3 or H4, the schematic is
untouched, and nothing is bought.

---

## 9. Phase B, gated

Phase B is the original question of this experiment: can received power be measured
repeatably in the available environment.

**Gate**: it needs a detector, a radio frequency source, an antenna or two and cables,
none of which is owned. It is not scheduled and no part of the Rev A decision set waits
on it.

| Phase B measurement | Needs |
| --- | --- |
| Repeated received power at a fixed geometry | detector, source, antennas |
| Effect of a person moving in the room | the same |
| Effect of moving an object | the same |
| Reconnection repeatability at radio frequency | cables and connectors |

What can be done before then, with the analyser alone and no purchase, is the
instrument and connector repeatability floor: repeat a transmission measurement through
a fixed arrangement, unplug and replug, and record the spread. That is worth doing when
the analyser is next available and it feeds the same uncertainty, I1.

---

## 10. Follow-up

- Record every reading in `results/EXP-005/`, which carries the empty tables.
- Apply section 7 as written. If a rule turns out to be unusable, say so and redo the
  experiment; do not adjust the rule against the data.
- Then update decision 0005, requirement R9 and open item H3 with the outcome.
- Phase A is a prerequisite for schematic re-capture, because two of the things that
  would be captured are what it decides.
