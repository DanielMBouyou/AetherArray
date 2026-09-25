# EXP-005 results

- Status: empty, awaiting Phase A
- Last reviewed: 2026-09-25

Protocol and decision rules in `experiments/EXP-005-repeatability-floor.md`. The rules
in its section 7 were fixed before any measurement and are not adjusted against the
data. A cell that was not measured stays `to measure`.

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

None of the decision rules applies unless all four pass.

| | Precondition | Threshold | Measured | Pass |
| --- | --- | --- | --- | --- |
| V1 | raw codes show at least two adjacent distinct values | at least 2 | to measure | to measure |
| V2 | within state spread, local path, condition C1 | at most 2 mV | to measure | to measure |
| V3 | source drift within one cycle | at most 0.5 mV | to measure | to measure |
| V4 | agreement between the two paths at rest | within 3 mV | to measure | to measure |

## 2. Main table

One row per path and condition, aggregated over the cycles. All voltages in mV. The dB
column uses the detector slope of $-25$ mV/dB and is a convenience, not a measurement.

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

Condition C3, far path. The knee is the shortest delay beyond which the mean stops
moving by more than 0.5 mV.

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

Applied from section 7 of the protocol. **Copy the rule that fired, do not paraphrase
it.**

| Question | Rule that fired | Outcome |
| --- | --- | --- |
| R9, the quiet window | to measure | keep, keep provisionally, demote, or escalate |
| H3, the converter on the board | to measure | keep, keep provisionally, or demote |
| C4, the temperature bus | to measure | mandatory scheduling outside the window, or not |
| C5, the grounding arrangement | to measure | H5 upgraded to a measured requirement, or not |

### Consequences to apply

Left blank until the outcome exists. Each of these is a document to edit, named here so
the follow-up is not reconstructed from memory.

| If | Then edit |
| --- | --- |
| R9 demoted | `docs/hardware/rev-a-requirements.md` R9, decision 0005 reopening conditions, `docs/architecture/control-architecture.md` section 5 |
| R9 escalated | decision 0005 reopens in full; the acquisition path is redesigned before re-capture |
| H3 demoted | `docs/architecture/control-architecture.md` sections 4.1 and 7, the connector line count, decision 0005 point 2 |
| C5 shows an effect | open item H5 in `docs/architecture/control-architecture.md` section 8 |

## 7. Phase B

Not started. Gated on a detector, a radio frequency source, antennas and cables, none
of which is owned. See section 9 of the protocol.
