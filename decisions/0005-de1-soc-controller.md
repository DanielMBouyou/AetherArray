# 0005. The Rev A controller is an external DE1-SoC

- Status: accepted, schematic re-capture required before layout
- Date: 2026-09-23
- Scope: the control path, the acquisition path, the digital interface on the radio frequency board, and the form of the learning track

## Question

What drives the Rev A array, records its measurements, and in what form is the learning
track posed?

## Context

Decision 0003 specified sixteen control lines from an STM32G0 Nucleo, with the
commanded word read back from the microcontroller's output register, and
`docs/hardware/rev-a-requirements.md` section 6 answered uncertainty I10 by stating that
this project has no need of an FPGA.

That answer addressed whether **beamforming** needs programmable logic. With an analogue
array it does not, and that part stands. It did not address what the **measurement**
needs, and decision 0002 had by then made unattended, repeatable, timestamped
measurement the figure of merit of the entire project.

## Options considered

### Option A: keep the microcontroller

Sixteen general purpose lines, the commanded word read back in software.

Upside: already captured, already costed, already owned, and no new toolchain. Downside:
the delay between applying a beam state and sampling the detector is subject to
interrupts and host traffic, so it jitters; the sixteen lines are written in sequence
rather than at one instant; and the timestamps come from a different clock than the
trigger. Each of those enters the data as scatter correlated with the measurement
sequence, which is the one kind of error this project cannot tolerate.

### Option B: external DE1-SoC, fabric for timing, processor for everything else

The fabric applies beam states, sequences, triggers and timestamps. The processor on
the same device orchestrates, stores and infers.

Upside: the settling delay is an exact number of clock cycles, all sixteen bits change
on one edge, one clock timestamps both the strobe and the conversion, the sequence runs
unattended, and the control lines can be held static during the sample window by
construction. Downside: gateware is new work this project has none of, the board is
external so the interface crosses a cable, and the schematic must be re-captured.

### Option C: DE1-SoC with the radio frequency parts moved onto it

Upside: no cable. Downside: destroys the two board separation that requirement R1
exists to protect, and puts a receive chain next to a large digital board. Rejected
without further analysis.

## Comparison

| Criterion | A | B | C |
| --- | --- | --- | --- |
| Settling delay repeatable to the clock | no | **yes** | yes |
| Sixteen bits applied at one instant | no | **yes** | yes |
| Trigger and timestamp share a clock | no | **yes** | yes |
| Control lines provably static while sampling | by convention | **by construction** | yes |
| Unattended sequencing without the host | no | **yes** | yes |
| New toolchain and gateware effort | none | **substantial** | substantial |
| Preserves the two board separation | yes | **yes** | **no** |
| Schematic re-capture needed | no | yes | yes |

## Evidence

No experimental evidence. Nothing is built, and no gateware exists.

- Manufacturer documentation, bibliography T6: the DE1-SoC expansion headers carry 36
  user pins connected directly to the Cyclone V device, at 3.3 V with protection
  diodes, plus 5 V and 3.3 V rails and grounds. The board carries an eight channel,
  twelve bit converter with a 0 V to 4.096 V input range, reachable from the fabric
  over a four wire serial interface.
- Vendor documentation, bibliography V1: the PE4259-63 in single pin control mode takes
  a nominal 3 V logic input and requires a supply on pin 6. **Its control input
  threshold and absolute maximum could not be read**, because the datasheet is a scanned
  image. Direct compatibility with a 3.3 V output is therefore **not demonstrated**.
- Internal: decision 0002, whose figure of merit is unattended recalibrations per hour,
  and whose central claim is about drift measured near the noise floor.
- Internal: the identifiability count of $2N-2$ in
  `docs/architecture/ml-calibration.md` section 3, unchanged by this decision.

## Decision

**Rev A is controlled by a DE1-SoC, external to the radio frequency board**, with the
partition, interface, acquisition path and record schema in
`docs/architecture/control-architecture.md`.

Three points are decided rather than left to implementation.

1. **A registered buffer sits on the radio frequency board**, supplied from the board
   3V3 rail and clocked by a single strobe. It bounds the switch control input to the
   switch's own supply, restores edges after the cable, removes cable skew, and makes
   the sixteen bit application synchronous at the board rather than at the cable.
   **It does not establish logic level compatibility**, and no such claim is made here:
   the switch input thresholds are unread and no buffer is selected. That is open item
   H1 in `docs/architecture/control-architecture.md` section 8, and it gates board
   release rather than the architecture.
2. **The detector is digitised on the radio frequency board**, not on the DE1-SoC, as a
   **precaution rather than a measured necessity**. The mechanism is real, a state
   correlated error imitates a calibration coefficient rather than looking like noise,
   but the magnitude of the pickup has not been measured. The decision rests on cost
   asymmetry: a few euro to fit, a board revision and a plausible looking wrong
   coefficient to omit and be wrong. The DE1-SoC converter is **kept as an independent
   path**, and EXP-005 compares the two before the board is released.
3. **The learning track is a Bayesian inverse problem**, formalised in
   `docs/mathematics/inverse-calibration.md`: the forward model and noise model are
   explicit physics, history enters only as a prior over the array state, and active
   selection maximises expected information gain. The first state model is diagonal;
   the full coupling matrix is a documented extension.

## Consequences

- Uncertainty I10 is answered differently from before, and the earlier answer is
  superseded rather than deleted. The FPGA earns its place through measurement
  determinism, not through beamforming.
- **The captured schematic no longer matches the architecture.** The interface symbol,
  the two registered buffers, the serial converter and its connector pins all change.
  The radio frequency topology does not. Re-capture is a follow-up task.
- The 2 by 13 connector becomes about 26 signal lines plus interleaved grounds, so a
  2 by 20.
- Gateware becomes project work that did not exist before: a beam state register, a
  sequencer, a trigger generator, a timestamp counter, a serial master and an I2C
  master. None of it is written here.
- The record schema in `docs/architecture/control-architecture.md` section 6 is now the
  contract for EXP-014 and EXP-015, and a session that does not produce those fields is
  not part of the dataset.
- Beam synthesis for Rev A is settled as an enumeration of 512 states against the
  estimated model, so the earlier scheduling of a surrogate pattern synthesis track is
  withdrawn; a surrogate is retained only as a control in the model free arm.
- The bill of materials gains a converter and two buffers and loses nothing. It has not
  been re-costed.

## Known limitations

The whole case rests on timing determinism mattering more than the effort of a new
toolchain, and that has not been measured. If EXP-005 shows the repeatability floor is
dominated by the environment rather than by control timing, option A would have been
adequate and this decision bought complexity for nothing. The cost of being wrong is
bounded, since the radio frequency design is unaffected either way.

No gateware exists, no converter is chosen, no buffer is chosen, and the current
capability of the expansion header rails has not been read.

The claim that an external board on a ribbon is acceptable beside a 2.44 GHz receive
chain is an engineering judgement, not a measurement. The ground strategy between the
two boards is an open item and needs settling before layout.

## Conditions for reopening

- If EXP-005 shows the repeatability floor is set by the environment and not by control
  timing, revisit whether the controller change earns its complexity. **This demotion is
  available without touching the radio frequency architecture**: requirement R9 and the
  local converter are both properties of the control path. What changes is the connector
  line count and which converter is used; the divider, the switched line chains, the
  element ports, the detector and the frequency are untouched. The fallback is option A
  with the DE1-SoC converter, and it costs a re-capture of the digital section only.
- If EXP-005 shows the two converter paths agree well inside the repeatability floor,
  demote the local converter to optional and use the DE1-SoC converter.
- If the expansion header cannot supply the board rails, the board takes its own supply
  and the grounding question is reopened with it.
- If gateware effort proves to dominate the schedule, fall back to option A for the
  first measurement campaign and keep the DE1-SoC for the unattended drift run, which
  is the part that actually needs it.
- If measured coupling makes the diagonal state model untenable, uncertainty I6, the
  inverse problem moves to the full matrix and the measurement counts are recomputed.
