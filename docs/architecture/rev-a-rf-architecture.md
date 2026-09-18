# Rev A RF architecture

- Status: selected and captured, dimensions still blocked on EXP-004
- Last reviewed: 2026-09-18

> **Captured on 2026-09-18.** The schematic is in `hardware/rev-a/`, the electrical
> rule check is clean, and the bill of materials in `hardware/rev-a/bom/` is exported
> from the captured design rather than estimated. One change was made during capture:
> the fitted switch count is **29, not 28**. Capture added `U900` to select between
> the analyser and the on board detector at the common node, because hard wiring both
> would load the path and split the signal whether or not the detector was in use.
> Cost is about 0.5 EUR and roughly 0.5 dB in the common arm. Section 6 below is
> otherwise unchanged.

One architecture, chosen and costed, so that schematic capture can start without
reopening a first-order topology question. Decision recorded in
`decisions/0003-rev-a-rf-architecture.md`.

This document does not contain a schematic or a layout, and does not attempt one.

---

## 1. What this has to reconcile

Four documents made commitments that were not all compatible.

| Source | Commitment | Status after this work |
| --- | --- | --- |
| `docs/hardware/rev-a-requirements.md` | R1 to R8, per element access and temperature telemetry cannot be retrofitted | **kept, and R1 is now satisfied by construction** |
| `decisions/0002-learning-as-a-drift-prior.md` | four elements minimum, unattended recalibration is the figure of merit | **kept, and it drives every choice below** |
| `docs/architecture/options.md` | analogue array, option A or C, no FPGA | **kept, option C selected in its switched line form** |
| `docs/hardware/bom-proposal.md` | two bit switched line, eight switches, one board carrying antennas, splitter and phase shifters | **partly superseded, see section 8** |

The conflict was concrete. The bill of materials proposed a single board integrating
the splitter, and `rev-a-requirements.md` section 3 showed that this form closes the
mutual coupling route permanently, and with it the unattended dataset that decision
0002 depends on.

---

## 2. Established, and assumed

Separated because the architecture is only as good as the first column.

### 2.1 Established

| Fact | Source | Consequence |
| --- | --- | --- |
| PE4259-63 covers 10 MHz to 3000 MHz, 0.35 dB insertion loss, 1.8 V to 3.3 V, SC-70-6, with on chip control logic | pSemi product page, distributor listing consulted 2026-09-18 | a switched line bit costs about 1 EUR of silicon rather than 5 |
| PE4259-63 is active, recommended for new designs, with more than 300000 units in distributor stock at 0.84 USD in unit quantity and 0.475 USD at 100 | distributor listing consulted 2026-09-18 | no availability risk on the part the whole design leans on |
| PE44820B-X is active, 328 units in stock, 13.09 USD in unit quantity, 32 lead 5 mm QFN | distributor listing consulted 2026-09-18 | four channels of it cost about 48 EUR, which is the entire project budget |
| PE44820 nominal band is 1.7 GHz to 2.2 GHz, with extended narrowband operation quoted from 1.1 GHz to 3.0 GHz | manufacturer product page | usable at 2.4 GHz only outside its specified band |
| PE4302 is discontinued; PE4312 is the pin compatible successor, 1 MHz to 4 GHz, 6 bit, 31.5 dB in 0.5 dB steps | manufacturer documentation consulted 2026-09-18 | any amplitude control provision must name PE4312, not the part most references still quote |
| ADL5390 is specified from 20 MHz to 2400 MHz | manufacturer product page | 2.4 GHz sits exactly on its upper limit |
| Mutual coupling calibration requires transmitting and receiving on element pairs | Aumann, Fenn and Willwerth 1989, bibliography A7 | per element connectors are a requirement, not a convenience |
| The rotating element field vector method needs at least three phase states, and its accuracy is limited by phase shifter resolution | bibliography A6 and A20 | phase resolution is a property of the baseline, not only of the beam |
| Half wavelength spacing at 2.4 GHz is 62.5 mm | calculation from $\lambda = c/f$ | a four element antenna board is about 250 mm long |
| MCP9808 gives about 0.25 degrees Celsius typical accuracy over its range, I2C, 8 pin | manufacturer documentation consulted 2026-09-18 | temperature telemetry costs about 1.5 EUR per point |
| AD8318 covers 1 MHz to 8 GHz, holds $\pm 1$ dB over a 55 dB range below 5.8 GHz, has a nominal slope of $-25$ mV/dB, a stability over temperature of $\pm 0.5$ dB, a single 5 V supply and about 68 mA typical current | manufacturer data sheet, revision E, bibliography V6, consulted 2026-09-18 | **the detector no longer constrains the working frequency, and its drift is a correctable term rather than an unknown** |

### 2.2 Assumed, and what would invalidate it

| Assumption | Why it is reasonable | How it falls | Effect |
| --- | --- | --- | --- |
| Working frequency is 2.4 GHz | licence exempt, instruments almost certainly reach it, antennas are small, FR4 is still usable | the network analyser does not cover it, EXP-004 | line lengths and patch dimensions change; **topology does not** |
| The network analyser has two ports covering the band | usual for any vector instrument | EXP-004 finds a one port instrument | the mutual coupling route closes, and R2 loses its value |
| PE4259 insertion loss at 2.4 GHz is near 0.5 dB rather than the quoted 0.35 dB | the quoted figure is not stated at this frequency | measurement | chain loss estimate moves by about 1 dB |
| Switch state to state repeatability is better than the measurement floor | CMOS switches are deterministic | EXP-005 and repeated switching | **if false, the drift experiment measures the switches, not the array** |
| Detector drift over a laboratory swing of a few degrees is far below the $\pm 0.5$ dB quoted over the full range | the quoted figure spans 125 degrees Celsius | the curve is strongly nonlinear near room temperature | more correction needed, which R4 already makes possible. **Inferred, not quoted: the data sheet gives the range figure, not a per degree slope** |
| FR4 line loss at 2.4 GHz is tolerable over the delay lengths needed | common practice at this frequency | electromagnetic simulation | more loss spread between phase states |
| Two board fabrication fits the cost share already budgeted | both boards are two layer and simple | quotation | budget pressure, see section 6 |

---

## 3. Phase control, compared

Ten axes, as required before a choice is defensible. Costs are for four channels in
unit quantities, converted at approximately 0.92 EUR per USD.

| Axis | P1 switched line, PE4259-63 | P2 digital phase shifter, PE44820B-X | P3 reflection type, varactor | P4 vector multiplier, ADL5390 | P5 beamformer core chip | P6 digital beamforming |
| --- | --- | --- | --- | --- | --- | --- |
| Frequency range | part covers 10 MHz to 3 GHz; band set by the delay lines, so narrowband by construction | 1.7 to 2.2 GHz specified, 1.1 to 3.0 GHz extended | narrowband, set by the printed hybrid | 20 MHz to 2400 MHz, at the limit | X and Ku band parts, wrong band | set by the receivers |
| Phase resolution | 45 degrees at three bits, 22.5 at four | 1.4 degrees, 8 bit | continuous | continuous, full 360 degrees | about 2.8 degrees | arbitrary |
| Insertion loss | about 3 dB estimated, six switches plus line, **to verify** | to verify, datasheet not machine readable | 2 to 4 dB, and it varies with phase | active, gain from about +5 dB to -30 dB | active | not applicable |
| Amplitude capability | none | none | none | **yes, full complex control** | yes | yes |
| Control interface | three logic lines per channel, direct from a microcontroller | serial or parallel | analogue voltage, needs a converter per channel | two analogue voltages per channel | serial | software |
| Calibration observability | **exact code word, fully deterministic, satisfies R5 directly** | exact code word | poor, nonlinear and temperature dependent | good, but the commanded value is analogue | exact | exact |
| Per element access | independent of the choice, one switch per channel | independent | independent | independent | usually integrated, harder to break out | native |
| PCB complexity | **high area**, delay lines dominate; two layer is enough | low area, fine pitch QFN | moderate, printed hybrid plus bias | moderate, needs a quadrature hybrid per channel | high | high |
| Cost, four channels | **about 20 EUR including the enable switches** | about 48 EUR | about 8 EUR | historically 60 EUR or more, to verify | out of budget | out of budget |
| Availability, 2026-09-18 | active, very deep stock | active, 328 in stock | generic parts | eval board listed, unit price to verify | not distributor friendly | not owned |

**P1 is selected.** The reasoning that settles it is not cost alone.

P2 is rejected on two counts that compound: it costs the entire budget, and at 2.4 GHz
it runs outside its specified band, so its one advantage, accuracy, is the thing that
becomes unspecified.

P3 is rejected for a reason the earlier bill of materials did not consider. A varactor
phase shifter has a temperature dependent phase characteristic. Decision 0002 commits
this project to measuring temperature dependent phase drift. Building the experiment
out of a component whose own drift is comparable to the effect under study would
confound the central result, and no amount of calibration recovers a confound of that
kind. It is the cheapest option and it is disqualified on scientific grounds.

P4 is the only option offering amplitude control, and it sits exactly on its specified
upper frequency limit at 2.4 GHz. Combined with analogue control and per channel
quadrature hybrids, it is not defensible for a first board.

P5 and P6 are excluded by `docs/hardware/rev-a-requirements.md` section 6 and by
`docs/architecture/options.md`, and nothing found here reopens them.

---

## 4. Amplitude control: decided, and decided against

**Rev A has phase control only. Gains are estimated and not corrected.**

| Argument | Weight |
| --- | --- |
| B2, B3, B5 and B6 all need commandable phase and element on and off, and none needs amplitude control | decisive |
| The primary metric is pointing error, which is driven by phase, not by gain | decisive |
| Element on and off is supplied by the enable switch, which is needed anyway for per channel isolation | removes the usual reason to fit an attenuator |
| The only compared option offering amplitude, P4, is at its band edge and over budget | removes the cheap route to it |
| Gain errors remain part of the $2N-2$ estimated parameters and are still measured | nothing is lost on the estimation side |

What this costs, stated rather than hidden: amplitude tapering is impossible, so
sidelobe level cannot be optimised, and the Rev A definition of a target calibrated
beam is written on pointing error and main lobe gain only. Sidelobe level is reported
as an observed quantity, never as a design target.

Architectural provision: a series passthrough per channel sized so that a PE4312
digital step attenuator can be fitted later without moving the rest of the chain. That
is a provision, not a fitted part, and it is not in the bill of materials.

---

## 5. The selected architecture

### 5.1 Block diagram

```
BOARD A  antenna board                  BOARD B  beamformer board

 patch 0 -- SMA-A0 ===jumper 0===> SMA-B0 --[EN 0]--[PS 0]--\
 patch 1 -- SMA-A1 ===jumper 1===> SMA-B1 --[EN 1]--[PS 1]---\
 patch 2 -- SMA-A2 ===jumper 2===> SMA-B2 --[EN 2]--[PS 2]---- [4:1 Wilkinson]
 patch 3 -- SMA-A3 ===jumper 3===> SMA-B3 --[EN 3]--[PS 3]---/        |
                                                                  SMA-SUM
                                                                     |
                                              +----------------------+-------------+
                                              |                                    |
                                     [AD8318 detector]                    to analyser port 2
                                              |
                                     analogue out to microcontroller

 EN n : one PE4259-63, throw 1 to the phase chain, throw 2 to a 50 ohm termination
 PS n : three cascaded bits of 45, 90 and 180 degrees, two PE4259-63 per bit

 one bit:   in --[SPDT]--+--[reference line]--+--[SPDT]-- out
                          \                  /
                           +--[delay line]--+
```

### 5.2 Why two boards

This is the single most important topology choice, and it is what makes R1 and R2 true
by construction rather than by addition.

| Consequence | Value |
| --- | --- |
| Every element terminates in its own connector | R1 and R2 satisfied natively; the mutual coupling route stays open |
| The four jumpers are in the signal path | EXP-007, the known cable error demonstration, becomes native instead of contrived, and the reconnection sensitivity metric becomes measurable by design |
| The beamformer board is independent of the antenna board | it survives a change of frequency, of antenna type, or a move to a different element set |
| Two smaller simple boards instead of one large dense one | keeps both inside ordinary fabrication tiers |
| Cost is four extra connector pairs and four cables | those are on the shared line of the lab accounting rule |

The risk is honest and worth stating: eight connectors and four cables add loss and add
drift sources. That drift is inside what EXP-010 measures, so it is not free, but it is
at least observable rather than hidden.

### 5.3 How each measurement is taken

| Measurement | Path | Unattended |
| --- | --- | --- |
| Sum port power, the cheap measurement | detector on the beamformer board into the microcontroller converter | **yes** |
| Sum port complex response, the expensive label for ML-B | analyser port 1 to a probe antenna, sum port to analyser port 2 | yes, once cabled |
| Per channel complex response, B2 | enable one channel, terminate the other three, read the sum port | **yes, switched electronically** |
| Element to element coupling, B6 | jumpers removed on the pair, analyser across two element connectors, remaining elements terminated through their enable switches | no, it needs recabling |
| Temperature | two MCP9808 on I2C | yes |

The third row is the one that matters most. It means the expensive label that supervises
the learned drift prior is obtained **without touching the hardware**, which is what
makes a dataset of order 100 sessions realistic.

### 5.4 Control interface

| Signal | Count | Direction | Note |
| --- | --- | --- | --- |
| Phase bit select | 12, three per channel | microcontroller to board | one line drives both switches of a bit, using the complementary control input |
| Channel enable | 4 | microcontroller to board | selects the phase chain or the 50 ohm termination |
| Detector output | 1 | board to microcontroller | analogue, into the converter |
| I2C clock and data | 2 | bidirectional | two MCP9808 |

Sixteen general purpose lines carry the entire commanded state, so the code word is
16 bits wide. R5 is satisfied without any extra component: the microcontroller output
data register is readable, so the commanded word is written and read back in software,
and R8 logs it with the detector reading, the temperature and the timestamp.

An STM32G0 Nucleo already owned supplies all of this.

### 5.5 Power rails

| Rail | Source | Consumers | Requirement |
| --- | --- | --- | --- |
| 5 V | Nucleo or USB | AD8318 | **single 5 V supply, 68 mA typical**, bibliography V6. Size the rail for 100 mA to leave margin |
| 3.3 V | Nucleo | 28 PE4259-63, 2 MCP9808 | PE4259 operates from 1.8 V to 3.3 V, microamp parts; MCP9808 about 200 microamp each |
| Ground | | | one plane on the beamformer board |

**The detector is 68 of the roughly 69 mA the board draws.** Everything else is
negligible, so the power budget is the detector budget, and a Nucleo powered from USB
supplies it with room to spare.

What the schematic has to provide, all of it derived from V6 rather than assumed:

| Item | Requirement | Why |
| --- | --- | --- |
| 5 V rail quality | local decoupling and a low noise feed, not a bare tap off the USB rail | the output is a slope of $-25$ mV/dB, so 25 mV of supply induced output error reads as a full 1 dB of apparent power |
| Analogue to digital reference | a stable reference, not a floating supply derived one | reference drift is indistinguishable from received power drift, and would enter EXP-015 as a physical result |
| Converter resolution | 12 bit over 3.3 V gives about 0.81 mV per step, so about **0.032 dB per step** | quantisation is not the limit; noise and reference stability are |
| Output span to plan for | 55 dB of usable range at $-25$ mV/dB is about 1.4 V of swing | fits inside the converter input range without attenuation or gain |
| Slope polarity | negative, more input power gives lower output voltage | the sign has to be right in firmware, and it is a classic source of an inverted calibration curve |
| Temperature sensor placement | one MCP9808 close to the detector | the $\pm 0.5$ dB stability figure is corrected empirically against logged temperature, so R4 is load bearing here, not advisory |

---

## 6. Candidate bill of materials

| Item | Part | Quantity | Unit | Total |
| --- | --- | --- | --- | --- |
| SPDT RF switch | PE4259-63 | 40 purchased, 28 fitted | about 0.50 EUR | about 20 EUR |
| Temperature sensor | MCP9808 | 2 | about 1.50 EUR | about 3 EUR |
| Logarithmic detector | AD8318, module form | 1 | about 12 EUR | about 12 EUR |
| Antenna board fabrication share | | 1 | about 8 EUR | about 8 EUR |
| Beamformer board fabrication share | | 1 | about 8 EUR | about 8 EUR |
| RF passives, terminations, bias components | | 1 set | about 8 EUR | about 8 EUR |
| Probe antenna for the transmit side | commercial 2.4 GHz | 1 | about 3 EUR | about 3 EUR |
| **Total** | | | | **about 62 EUR** |

SMA connectors and the four jumpers are not counted here. Under the lab accounting
rule they are bought once by whichever radio frequency project needs them first. **If
this project buys them first, this list is over the rule** and something has to move.

### 6.1 What may be cut, and what may not

This distinction exists because an earlier draft of this document offered the third
phase bit as the cheapest saving, which contradicted section 8, where the same bit is
justified as necessary. A choice cannot be load bearing in one section and spare change
in another.

**Neutral levers.** These change cost without touching the architecture, and together
free about 19 EUR.

| Lever | Saving | What it costs |
| --- | --- | --- |
| Buy 32 switches rather than 40 | about 4 EUR | four spares instead of twelve, so less tolerance for rework |
| Use an antenna already owned as the transmit probe | about 3 EUR | a less well characterised probe, which mostly cancels in relative measurements |
| Account the detector on the shared line | about 12 EUR | none to this project. The detector is a general purpose scalar receiver and serves the radio frequency modelling project equally, so the lab rule already allows it to be counted once |

**Not levers.** Each of these reopens a recorded decision, and none is a budget
substitution.

| Change | What it reopens |
| --- | --- |
| Fewer than four elements | **decision 0002.** The learning track has no room below four, see `ml-calibration.md` section 8 |
| Fewer than three phase bits | **decision 0003 and the measurement count comparison itself**, see section 8 and section 8.1 |
| Removing the per element connectors | **decision 0002 through R1 and R2**, and the unattended dataset with it |
| Removing the temperature sensor at the detector | gate G2 interpretation, because the detector stability figure is corrected against logged temperature |

If the budget cannot be met with the neutral levers alone, the correct response is to
delay the order, not to quietly shrink the array.

Prices are indicative and were taken from distributor listings on 2026-09-18. They are
re-checked before ordering, and nothing is ordered before section 7 clears.

---

## 7. Frozen now, and blocked

The distinction that matters: **topology is frozen, dimensions are not.** Delay line
lengths and patch geometry are layout parameters, not schematic ones, so schematic
capture can proceed while EXP-004 is still outstanding.

### 7.1 Frozen, safe to capture

| | Choice |
| --- | --- |
| F1 | Four elements |
| F2 | Two boards, antenna and beamformer, joined by four equal length jumpers |
| F3 | One enable switch per channel selecting the phase chain or a 50 ohm termination |
| F4 | Phase control only, no amplitude control, with a provision for a PE4312 later |
| F5 | Switched line phase shifting, three bits of 45, 90 and 180 degrees, PE4259-63 |
| F6 | Two measurement paths, the analyser for complex labels and an on board detector for unattended scalar readings |
| F7 | Sixteen control lines from an STM32G0, commanded word read back from the output register |
| F8 | 5 V input, 3.3 V logic rail, single ground plane |

### 7.2 Blocked by EXP-004, the instrument audit

| | Question | What it changes |
| --- | --- | --- |
| E1 | Does the analyser cover 2.4 GHz | the working frequency, therefore every delay line length and patch dimension. Topology is unaffected |
| E2 | Does the analyser have two ports | whether B6 can run at all, and therefore how much R2 is worth |
| E3 | Is phase measurable, gate G1 | whether B5 joins the comparison |
| E4 | Is there a source able to drive the probe antenna, or must the analyser supply it | whether the radiated path can run while the analyser is busy |

### 7.3 Blocked by EXP-005, the repeatability trial

| | Question | What it changes |
| --- | --- | --- |
| E5 | Does the detector path reach the repeatability needed for unattended runs | if not, every measurement needs the analyser, the unattended dataset dies, and decision 0002 fails with it |
| E6 | Is switch state repeatability below the measurement floor | if not, the drift experiment measures the switches |

### 7.4 Closed since the first draft

| | Item |
| --- | --- |
| E7 | **Resolved.** The AD8318 figures were confirmed against revision E of the manufacturer data sheet, bibliography V6. They are recorded in section 2.1 and turned into schematic requirements in section 5.5. Three consequences follow. The detector works anywhere from 1 MHz to well past any band this project would choose, so it does not constrain the outcome of EXP-004. Its temperature stability is a bounded, correctable term rather than an unknown, which removes it as a confound on gate G2, **provided a temperature sensor sits next to it**. And the 68 mA figure makes the power budget trivially satisfied by the Nucleo. This item no longer blocks ordering |

---

## 8. What this supersedes

Stated explicitly, because `docs/hardware/bom-proposal.md` is still read as current.

| Superseded | Replaced by | Reason |
| --- | --- | --- |
| Two bit phase shifting, 90 degree steps | **three bits, 45 degree steps** | two bits gives a worst case quantisation error of 45 degrees, which degrades the rotating element field vector baseline itself. That baseline is the reference the entire measurement count comparison is quoted against, so crippling it corrupts the comparison rather than the beam. Separately, with $Q$ phase states and $N$ elements the exhaustive search over commands costs $Q^{\,N-1}$, which is 64 at two bits and 512 at three, crossing the threshold in `ml-calibration.md` section 4 below which the pattern synthesis track is not worth running |
| Eight RF switches at about 2.50 EUR each | **28 fitted, 40 purchased, at about 0.50 EUR each** | the old line assumed a selector topology and a price five times the current one. A cascaded bit switched line needs six switches per channel at three bits. The total cost lands in the same place only because PE4259-63 is far cheaper than assumed |
| One board carrying the antennas, the splitter and the phase shifters | **two boards joined by per element jumpers** | the integrated form closes R1 and R2 permanently, as shown in `rev-a-requirements.md` section 3 |
| "Analogue phase shifter integrated circuit, often 20 EUR or more per channel" | **PE44820B-X at 13.09 USD in unit quantity** | the real figure, recorded so the rejection rests on evidence. The part is still rejected, on budget and on band edge, not on a guessed price |
| "Varactor based phase shifter, around 10 EUR, medium risk" | **rejected on scientific grounds** | it is cheaper than stated, and it injects temperature dependent phase drift into the experiment that measures temperature dependent phase drift |
| Any reference to PE4302 | **PE4312** | PE4302 is discontinued |

`docs/hardware/bom-proposal.md` has been marked superseded on these points rather than
deleted, as `CONVENTIONS.md` section 2 requires.

### 8.1 Two bit operation is a reopening, not a fallback

Recorded plainly because an earlier draft of this document treated it as both.

Two bit operation is retained in exactly one place: as a configuration the hardware can
be built in, if a later decision chooses it. It is **not** a budget substitution, it is
**not** a fallback, and it is not listed among the neutral levers in section 6.1.

Building or operating Rev A at two bits has these effects, and any of them alone is
enough to require a new decision record.

| Effect | Consequence |
| --- | --- |
| Worst case quantisation error rises from 22.5 to 45 degrees | at that magnitude the pattern is degraded rather than merely imperfect, see `docs/mathematics/formulation.md` section 4 |
| The rotating element field vector baseline is degraded | B3 is the reference every measurement count in `ml-calibration.md` sections 2 and 3 is quoted against. Degrading the reference does not make the learned method look better honestly, it makes the comparison meaningless |
| $Q^{\,N-1}$ falls from 512 to 64 | below the threshold in `ml-calibration.md` section 4, so the pattern synthesis track ML-D stops being worth running and has to be withdrawn rather than quietly reported |
| The benchmark contract changes | `benchmarks/specification.md` requires the bit count to be reported with every result, so published curves taken at three bits and at two bits are not comparable and may not be plotted together |

If two bits is ever chosen, decision 0003 is superseded, the affected sections of
`ml-calibration.md` are recomputed, and any measurement count result already obtained
at three bits is reported separately rather than merged.
