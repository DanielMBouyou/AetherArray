# Rev A requirements imposed by the calibration experiments

- Status: proposal; ordering is gated by decision 0006
- Last reviewed: 2026-09-25

What the first board must expose so that the experiments in
`docs/architecture/ml-calibration.md` remain possible. Nothing here is about routing
or schematic capture. It is about capabilities that are cheap to include now and
impossible to add later.

---

## 1. The principle

Algorithms can be replaced after the board exists. Observability cannot. Every
requirement below is judged on one question: **if Rev A omits this, is the experiment
recoverable without a new board?**

A second principle follows from `docs/architecture/ml-calibration.md` section 7. The
learned drift prior is limited by the number of labelled calibration pairs the rig can
produce, so the figure of merit for Rev A is **unattended calibrations per hour**, not
performance in any single calibration.

---

## 2. Requirements

| ID | Requirement | Enables | Retrofittable | Added cost |
| --- | --- | --- | --- | --- |
| R1 | Each element individually accessible at a connector, upstream of any on board combining | B2, B6, per element characterisation, all labels measured on hardware | **no** | about 6 EUR |
| R2 | Ability to drive one element and receive on another, using the two port analyser through R1 | B6, the mutual coupling route, therefore the unattended dataset | **no** | 0 EUR beyond R1 |
| R3 | A permanently wired scalar power sense at the sum port, **digitised on the board** and read by the controller | unattended repeat measurement without occupying the analyser | partly, as an external add on | about 12 EUR for the detector, plus a converter added by decision 0005 |
| R4 | At least one temperature sensor on the board, sited near the phase shifting network, and one near the detector | separates array drift from instrument drift, supplies the ML-B input | **no** | about 2 EUR |
| R5 | Commanded state written and read back as a code word, logged with every measurement | correct labelling of training data, since realised phase is not the requested phase | yes, in gateware | 0 EUR |
| R6 | Element count of at least four | the ML track has no room at $N = 2$, see the architecture document section 8 | **no** | as costed |
| R7 | A stable reference channel, identified and documented | every method here estimates relative quantities, so common mode drift is otherwise inseparable | **no** | 0 EUR |
| R8 | Timestamped machine readable logging of code word, detector reading, temperature, and a connector handling flag. **The record schema is fixed in `docs/architecture/control-architecture.md` section 6** | the drift dataset, which cannot be reconstructed after the fact | yes, in gateware | 0 EUR |
| R9 | The beam state applied at one instant, the control lines static while the detector is sampled, and the trigger and timestamp taken from one clock | **added by decision 0005.** Removes timing scatter correlated with the commanded state, which would otherwise imitate a calibration coefficient. **Adopted as a precaution; EXP-005 Phase A tests it against rules fixed in advance and can keep, demote or escalate it** | **no, this is why the controller changed.** It can however be demoted without disturbing the radio frequency design, because it is a property of the control path alone | 0 EUR in parts, gateware effort |

R1 and R2 are the same physical decision seen twice, and they are the decisive ones.

---

## 3. The decision that must be taken before the board is frozen

> **Taken, on 2026-09-18, by decision 0003.** Rev A is two boards joined by four per
> element jumpers, so R1 and R2 hold by construction rather than by addition. The
> analysis below is kept because it is the argument that forced the choice, and
> because it states what would be lost if the two board split were ever undone.

`docs/hardware/bom-proposal.md` function 2 proposes one board carrying the four
antennas, the splitter and the phase shifters. Read literally, that closes R1: with
the splitter integrated and no per element connector, no instrument can ever address a
single element, and the following become impossible without a new board.

| Closed by an integrated splitter with no per element access |
| --- |
| B2, the element by element baseline |
| B6, the mutual coupling method, whose only stated restriction is transmit and receive on element pairs |
| Any hardware measured label for a per element quantity |
| The unattended drift dataset, therefore the ML-B track, therefore the project's central claim |

The alternative is to bring each element out to its own connector and combine
externally, or to fit the combiner as a populate option. Cost is about four connectors
and some board area.

**This is the single highest leverage line in this document.** The mutual coupling
route is the only calibration path that needs no external probe, no positioner and no
operator, which is exactly what makes a dataset of order 100 sessions achievable on a
personal bench.

---

## 4. Reconciling with the budget rule

The private budget rule is 50 to 70 EUR of new hardware per project. The bill of
materials already stands at about 67 EUR. Adding R1 and R4 takes it to about 75 EUR,
which breaks the rule.

The proposed resolution is a swap rather than an increase:

| Change | Effect on total |
| --- | --- |
| Add per element connectors, R1 | about +6 EUR |
| Add temperature sensing, R4 | about +2 EUR |
| Defer the stepper motor and positioner set to a later purchase | about -15 EUR |
| **Revised total** | **about 60 EUR** |

The justification for deferring the positioner is that it serves pattern measurement,
which is a validation step, whereas R1 and R4 serve the dataset, which gates the
central claim. The positioner can be bought at any later date and bolted on. The
connectors cannot be added to a fabricated board.

The cost is real and is stated rather than hidden: without the positioner, Rev A
measures at the sum port and between element pairs, and cannot produce a full radiation
pattern. EXP-007, the cable error demonstration, becomes a few manual points rather
than a swept pattern.

---

## 5. The detector drift trap

Gate G2 asks whether array drift over hours exceeds the repeatability floor. That
question is only answerable if the measuring chain drifts less than the array does.

The part selected for R3 by decision 0003 is the AD8318. Its figures are now
**[established]** against revision E of the vendor data sheet, bibliography V6,
consulted 2026-09-18.

| Figure | Value | What it settles here |
| --- | --- | --- |
| Frequency range | 1 MHz to 8 GHz | the detector does not constrain the working frequency, so EXP-004 cannot invalidate this part |
| Accuracy | $\pm 1$ dB over a 55 dB range below 5.8 GHz | ample at any band this project would choose |
| Logarithmic slope | nominally $-25$ mV/dB | 55 dB of range maps to about 1.4 V of output swing |
| Stability over temperature | $\pm 0.5$ dB | bounded over the full 125 degree Celsius span, therefore small over a laboratory swing, and correctable in any case |
| Supply | single 5 V, about 68 mA typical | the whole board draws about 69 mA. Supplied from the controller's expansion header if its current limit allows, which is an open item in `docs/architecture/control-architecture.md` section 8 |

**The trap is closed, but only by R4.** The detector's own drift is bounded and
correctable rather than unknown, which removes it as a confound on gate G2, and the
correction is empirical against logged temperature. That makes the temperature sensor
beside the detector load bearing: without it the $\pm 0.5$ dB stays an uncorrected term
and a null result on G2 becomes uninterpretable again, exactly as feared. R4 is
therefore mandatory, not advisable, and it was already marked as not retrofittable.

What remains open is not the part but the chain: EXP-005 still has to show that the
whole measuring path, detector included, repeats well enough for unattended running.

---

## 6. What Rev A does not need

Stated so that the board is not made expensive for reasons that do not survive the
analysis.

| Not required | Reason |
| --- | --- |
| More than three phase bits per channel | **corrected on 2026-09-18.** This row previously said more than two, which decision 0003 contradicts. Three bits is required, not optional: two bits degrades the B3 baseline that every measurement count is quoted against, and it drops $Q^{\,N-1}$ below the threshold that makes track M5 worth running. A fourth bit benefits only M5 and is not required |
| Continuous analogue phase shifters | the quantisation is a study subject, and every method above tolerates coded states provided R5 holds |
| Coherent multi channel reception | the digital route, option B, is not selected, and no method above needs it |
| ~~An FPGA~~ | **superseded on 2026-09-23 by decision 0005.** The statement was right about beamforming and wrong about measurement. An analogue array needs no programmable logic to form a beam; the drift experiment needs it to apply a beam state at one instant, hold the control lines static while sampling, and timestamp the trigger from one clock. Uncertainty I10 is re-answered there |
| An anechoic environment | the mutual coupling and sum port routes are conducted or near field, and are far less sensitive to the room than pattern measurement |

---

## 7. Open gates on this document

| Gate | Blocks | Settled by |
| --- | --- | --- |
| G1, can phase be measured | whether B5 is available at all, and how R1 is exercised | EXP-004. **Closed 2026-09-23 by decision 0004**: phase is measurable |
| G2, is drift measurable above the floor | **whether R1, R3, R4 and R8 are worth their cost** | EXP-005 then EXP-010. Since decision 0006 the floor half is answered before fabrication and the drift half after it |
| G3, element count and bit count | R6, and the scale of the switch budget | **closed 2026-09-18 by decision 0003**: four elements, three bits |
| G5, budget | the swap proposed in section 4 | costing at order time |

Nothing here should be ordered before G1 and G2 are answered. Both are answerable with
instruments already owned.

**Superseded on 2026-09-25 by decision 0006.** G1 is answered. G2 is not answerable with
instruments already owned: its floor needs EXP-005 Phase B, which needs a detector,
antennas and interconnect, and its drift half needs the built array. Purchases are
staged by class there, and the drift half gates the learning track rather than the
order.
