# EXP-005 results

- Status: preparation logged, no measurement taken, C1 not executed
- Last reviewed: 2026-09-28

The protocol and its decision rules are in `experiments/EXP-005-repeatability-floor.md`.
The rules in its section 7 were fixed before any measurement, and they don't get
adjusted to fit the data. A cell that hasn't been measured stays `to measure`.

---

## Preparation log

These aren't measurements. They record work done away from the bench, so the session
itself is shorter, and so nobody repeats a lookup that already failed.

### P1, 2026-09-25: C1 not executed

C1 means wiring a source to a board, loading a configuration and reading a thermometer.
None of that has happened yet. **Every field in sections 0 to 6 below is still
`to measure`, and no validity precondition has been established.**

### P2, 2026-09-25: toolchain and board reachability

| Check | Result |
| --- | --- |
| Design software installed | **yes**, Quartus 17.1, which covers the device on this board |
| Any programmer ever attached to this computer | **no.** No programmer vendor identifier has ever been enumerated here |
| Design project or converter example on this computer | none found |

The second row fits what `results/EXP-004/` found for the instruments: no lab hardware
has ever been plugged into this machine. So the harness has to be built and loaded from
scratch, and the first bench session starts with getting the board to come up at all.

### P3, 2026-09-25: item B1, the analogue input path, **advanced but not closed**

Protocol item B1 asks for the analogue input header, its channel assignment, any
circuit in front of the converter, and the safe input range, all taken from the board
documentation instead of assumed.

| Established | Value |
| --- | --- |
| Converter | LTC2308, eight channels, 12 bit, up to 500 ksps |
| Input range quoted at the header | 0 V to 4.096 V |
| Converter internal reference | 2.5 V |
| Serial interface signal names | chip select, data in, data out and clock, at 3.3 V |

| Still required | Why it matters |
| --- | --- |
| The header reference designator and pin by pin channel assignment | wiring cannot be done without it |
| Whether any divider, buffer, filter or protection network sits between header and converter | see the discrepancy below |
| The absolute maximum input voltage at the header | safety of the source connection |

**Something to sort out before wiring anything.** The converter has a 2.5 V internal
reference, but the header range is quoted as 0 V to 4.096 V. Both can only be true if
something sits in between: either an external reference, or attenuation in front of the
converter input. **So there's probably a circuit there**, and catching exactly that is
what B1 was written for.

If it's a resistive divider, that matters for the source specification S1. The
converter's sampling capacitor would then see the divider's output impedance, not the
source's. So an S1 source that's stiff at the header could still be driving the
converter through a high impedance. If that happens, the sample rate gets lowered until
the reading stops depending on it. The operator can check this directly by sweeping the
rate and watching the mean.

**This doesn't change any threshold or decision rule.** It's just B1 doing its job.

Two attempts to download the board's user manual from mirror sites failed here, one on
a timeout and one on a dropped connection. **The operator has the manual locally**, so
closing B1 is a matter of looking up a page, not doing research.

### P4, 2026-09-25: item B2, the converter example

Not picked yet. Published examples exist for this exact board and converter, including
a university lab note written for this board and a separate course tutorial, and the
board maker ships demos too. **The operator picks one, and writes down which one and
its version**, as B2 requires. None of them has been read or tested here.

---

## 0. Setup as built

Filled in once, at the start of Phase A.

| Item | Record |
| --- | --- |
| Date, session identifier | to measure |
| B1, analogue input header and channels used, and any scaling in front of them | to measure |
| B2, converter example used, and its version | to measure |
| B5, room thermometer available | to measure |
| DE1-SoC board 1, identifier | to measure |
| DE1-SoC board 2, identifier | to measure |
| Ribbon length and type | to measure |
| Source realisation chosen, from S1 | to measure |
| Source level as measured | to measure |
| Source impedance as built | to measure |
| Converter sample rate used | to measure |
| Harness version identifier | to measure |
| Room temperature at start | to measure |

## 1. Validity preconditions

None of the decision rules counts unless all four of these pass.

| | Precondition | Threshold | Measured | Pass |
| --- | --- | --- | --- | --- |
| V1 | raw codes show at least two adjacent distinct values | at least 2 | to measure | to measure |
| V2 | within state spread, local path, condition C1 | at most 2 mV | to measure | to measure |
| V3 | source drift within one cycle | at most 0.5 mV | to measure | to measure |
| V4 | agreement between the two paths at rest | within 3 mV | to measure | to measure |

## 2. Main table

One row per path and condition, averaged over the cycles. All voltages are in mV. The dB
column uses the detector slope of $-25$ mV/dB. It's there for convenience, and it isn't
a measurement.

| Path | Condition | Mean | Within state spread | Between state spread | State correlated error | Equivalent dB | Cycles |
| --- | --- | --- | --- | --- | --- | --- | --- |
| local | C1 static | to measure | to measure | to measure | to measure | to measure | to measure |
| local | C2 active | to measure | to measure | to measure | to measure | to measure | to measure |
| local | C3 quiet window | to measure | to measure | to measure | to measure | to measure | to measure |
| local | C4 bus only | to measure | to measure | to measure | to measure | to measure | to measure |
| local | C5 ground strap | not run, or to measure | to measure | to measure | to measure | to measure | to measure |
| far | C1 static | to measure | to measure | to measure | to measure | to measure | to measure |
| far | C2 active | to measure | to measure | to measure | to measure | to measure | to measure |
| far | C3 quiet window | to measure | to measure | to measure | to measure | to measure | to measure |
| far | C4 bus only | to measure | to measure | to measure | to measure | to measure | to measure |
| far | C5 ground strap | not run, or to measure | to measure | to measure | to measure | to measure | to measure |

## 3. Settling sweep

Condition C3, far path. The knee is the shortest delay after which the mean stops moving
by more than 0.5 mV.

| Strobe to conversion delay | Mean, local | Mean, far | Difference |
| --- | --- | --- | --- |
| 1 us | to measure | to measure | to measure |
| 3 us | to measure | to measure | to measure |
| 10 us | to measure | to measure | to measure |
| 30 us | to measure | to measure | to measure |
| 100 us | to measure | to measure | to measure |
| 300 us | to measure | to measure | to measure |
| 1 ms | to measure | to measure | to measure |
| 3 ms | to measure | to measure | to measure |
| 10 ms | to measure | to measure | to measure |

**Settling interval selected for the sequencer**: to measure.

## 4. Reconnection

| Event | Path | Mean before | Mean after | Shift |
| --- | --- | --- | --- | --- |
| ribbon replug 1 | far | to measure | to measure | to measure |
| ribbon replug 2 | far | to measure | to measure | to measure |
| ribbon replug 3 | far | to measure | to measure | to measure |
| ribbon replug 4 | far | to measure | to measure | to measure |
| ribbon replug 5 | far | to measure | to measure | to measure |
| analogue lead replug 1 | local | to measure | to measure | to measure |
| analogue lead replug 2 | local | to measure | to measure | to measure |
| analogue lead replug 3 | local | to measure | to measure | to measure |

## 5. Sessions

| Session | Date | Room temperature, start and end | Mean, far, C3 | Mean, local, C3 | Elapsed |
| --- | --- | --- | --- | --- | --- |
| 1 | to measure | to measure | to measure | to measure | to measure |
| 2 | to measure | to measure | to measure | to measure | to measure |
| 3 | to measure | to measure | to measure | to measure | to measure |

## 6. Outcome

Applied from section 7 of the protocol. **Copy the rule that fired word for word. Don't
paraphrase it.**

| Question | Rule that fired | Outcome |
| --- | --- | --- |
| R9, the quiet window | to measure | keep, keep provisionally, demote, or escalate |
| H3, the converter on the board | to measure | keep, keep provisionally, or demote |
| C4, the temperature bus | to measure | mandatory scheduling outside the window, or not |
| C5, the grounding arrangement | to measure | H5 upgraded to a measured requirement, or not |

### Consequences to apply

Left blank until there's an outcome. Each one is a document to edit, named here so the
follow up doesn't have to be pieced together from memory.

| If | Then edit |
| --- | --- |
| R9 demoted | `docs/hardware/rev-a-requirements.md` R9, decision 0005 reopening conditions, `docs/architecture/control-architecture.md` section 5 |
| R9 escalated | decision 0005 reopens in full; the acquisition path is redesigned before re-capture |
| H3 demoted | `docs/architecture/control-architecture.md` sections 4.1 and 7, the connector line count, decision 0005 point 2 |
| C5 shows an effect | open item H5 in `docs/architecture/control-architecture.md` section 8 |

## 7. Phase B

Not started. It needs a detector, antennas and cables, and none of them is owned. It
doesn't need a separate RF source: decision 0006 notes that the analyser already plays
that role. What each purchase waits for is in decision 0006, and the rest is in section
9 of the protocol.
