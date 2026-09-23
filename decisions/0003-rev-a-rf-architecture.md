# 0003. Rev A is a two board, phase only, switched line array at three bits

- Status: accepted; **control path superseded by decision 0005**, frequency frozen by decision 0004, dimensions blocked on the stack-up
- Note: the radio frequency architecture below stands unchanged. The controller named in it is an STM32G0 and is now a DE1-SoC, and the schematic needs re-capturing to match. The text is kept as written, because a decision record says what was decided at the time.
- Date: 2026-09-18
- Scope: the first radio frequency hardware revision, its topology, phase control and control interface

## Question

Which radio frequency architecture should Rev A have, in enough detail that schematic
capture can begin without a first-order topology choice being reopened later?

## Context

Decision 0002 committed the project to a learned drift prior, whose figure of merit is
unattended recalibrations per hour, and to requirements R1 to R8 in
`docs/hardware/rev-a-requirements.md`, of which per element access and temperature
telemetry cannot be retrofitted.

`docs/hardware/bom-proposal.md` predates that and proposes a single board integrating
the antennas, the splitter and two bit switched line phase shifters. Those two
positions are not compatible: an integrated splitter with no per element connector
closes the mutual coupling route permanently, and the unattended dataset with it.

The instrument audit, EXP-004, has still not been run, so the working frequency is not
settled.

## Options considered

### Option A: single board, two bit switched line, as previously proposed

Cheapest to fabricate and already costed.

Upside: least work. Downside: it forecloses R1 and R2, and two bit quantisation
degrades the rotating element field vector baseline that the whole measurement count
comparison is referenced to.

### Option B: two boards, three bit switched line, phase only

Antennas and connectors on one board, switches and combiner on another, joined by four
jumpers. Phase control from cascaded switched line bits.

Upside: per element access exists by construction, the cable error experiment and the
reconnection metric become native, the beamformer board survives a change of frequency,
and per channel isolation is switched electronically so the expensive label is obtained
without touching the hardware. Downside: eight connectors and four cables add loss and
drift, and the delay lines need board area.

### Option C: integrated digital phase shifter per channel

One PE44820B-X per channel gives 1.4 degree resolution.

Upside: accuracy, small area. Downside: about 48 EUR for four channels, which is the
whole budget, and 2.4 GHz lies outside its specified 1.7 GHz to 2.2 GHz band, so the
accuracy that justifies the price becomes unspecified at the frequency we would use it.

### Option D: continuous phase by reflection type varactor shifter

Cheapest of all in parts, about 8 EUR for four channels.

Upside: cost, continuous control. Downside: its phase characteristic is temperature
dependent, and this project exists to measure temperature dependent phase drift.

### Option E: decide nothing until EXP-004 has run

Upside: no speculation about frequency. Downside: the audit settles dimensions, not
topology, and none of the choices above depends on the exact frequency. Waiting buys
nothing and delays everything.

## Comparison

| Criterion | A | B | C | D | E |
| --- | --- | --- | --- | --- | --- |
| Satisfies R1 and R2 | no | **yes, by construction** | yes, if connectors added | yes, if connectors added | not applicable |
| Cost, four channels | about 20 EUR | about 20 EUR | about 48 EUR | about 8 EUR | none |
| Degrades the reference baseline | **yes, at two bits** | no | no | no | not applicable |
| Confounds the drift experiment | no | no | no | **yes** | no |
| Within specified frequency band at 2.4 GHz | yes | yes | **no** | yes | not applicable |
| Commanded state is an exact code word, R5 | yes | yes | yes | **no, analogue** | not applicable |
| Unblocks schematic capture | yes | **yes** | yes | yes | **no** |
| Main risk | forecloses the project's central claim | connector loss and drift | budget and band edge | scientific confound | delay with no benefit |

## Evidence

No experimental evidence, since nothing is built. The choice rests on distributor and
manufacturer documentation consulted on 2026-09-18, and on results already recorded in
this repository.

- Manufacturer and distributor listing: PE4259-63, 10 MHz to 3000 MHz, 0.35 dB
  insertion loss, 1.8 V to 3.3 V, SC-70-6, active and recommended for new designs,
  0.84 USD in unit quantity and 0.475 USD at 100, with more than 300000 units in stock.
- Distributor listing: PE44820B-X, active, 328 in stock, 13.09 USD in unit quantity,
  32 lead 5 mm QFN. Manufacturer product page: nominal band 1.7 GHz to 2.2 GHz,
  extended narrowband operation 1.1 GHz to 3.0 GHz, 8 bit, 1.4 degree steps.
- Manufacturer documentation: PE4302 discontinued, PE4312 pin compatible successor,
  1 MHz to 4 GHz, 6 bit, 31.5 dB in 0.5 dB steps.
- Manufacturer product page: ADL5390 specified from 20 MHz to 2400 MHz.
- Manufacturer documentation: MCP9808, about 0.25 degrees Celsius typical accuracy,
  I2C.
- Internal result: the measurement count and observability analysis in
  `docs/architecture/ml-calibration.md` sections 2 to 4, and the threshold on
  $Q^{\,N-1}$ that makes the pattern synthesis track worth running.
- External source: Aumann, Fenn and Willwerth 1989, bibliography A7, for the element
  pair requirement that forces per element connectors.
- Unverified technical opinion, labelled as such: the estimate of about 3 dB chain
  insertion loss at three bits, and the assumption that PE4259 loss at 2.4 GHz is near
  0.5 dB rather than the quoted 0.35 dB, which is not stated at that frequency.

## Decision

Rev A is **option B**: two boards, four elements, phase control only, switched line
phase shifting at three bits of 45, 90 and 180 degrees using PE4259-63, one enable
switch per channel selecting the phase chain or a 50 ohm termination, an on board
logarithmic detector at the sum port alongside an analyser path, sixteen control lines
from an STM32G0 with the commanded word read back from the output register, and two
MCP9808 temperature sensors.

Amplitude control is deliberately absent. Gains are estimated and not corrected, and a
passthrough is sized so a PE4312 can be fitted later without moving the chain.

Full detail, including the block diagram, interfaces, rails and bill of materials, is
in `docs/architecture/rev-a-rf-architecture.md`.

## Consequences

- Schematic capture can begin now. Delay line lengths and patch geometry are layout
  parameters and stay open until EXP-004 fixes the frequency.
- The per channel complex label needed by ML-B is obtained by electronic switching,
  with no hardware handling, which is what makes a dataset of order 100 sessions
  realistic.
- Sidelobe level cannot be optimised at Rev A and is reported as an observed quantity,
  never as a design target.
- The four jumpers put connectors in the signal path. EXP-007 and the reconnection
  sensitivity metric become native experiments rather than contrived ones.
- `docs/hardware/bom-proposal.md` is superseded on five points, listed in section 8 of
  the architecture document.
- Nothing is ordered until EXP-004 and EXP-005 have run.
- The detector is settled. Revision E of the AD8318 data sheet, bibliography V6, gives
  1 MHz to 8 GHz, $\pm 1$ dB over 55 dB below 5.8 GHz, a nominal $-25$ mV/dB slope,
  $\pm 0.5$ dB stability over temperature, a single 5 V supply and about 68 mA typical.
  Consequences: the detector does not constrain the working frequency, so it is
  unaffected by whatever EXP-004 returns; its drift becomes a correctable term rather
  than a confound, provided a temperature sensor sits beside it; and the board draws
  about 69 mA in total, which a Nucleo supplies without help.

## Known limitations

The architecture is chosen from documentation, not from measurement, and the two
figures it leans on hardest are both estimates: the chain insertion loss at three bits,
and the state to state repeatability of the switches. The second is the more dangerous.
If switch repeatability is not well below the measurement floor, the drift experiment
measures the beamformer rather than the array, and the result would look like a
physical finding.

Three bits leaves a worst case quantisation error of 22.5 degrees, which is visible in
the pattern. That is accepted, and the quantisation study is part of the project.

The choice assumes the working frequency will be near 2.4 GHz. If EXP-004 forces a
large move, the delay lines and the antennas are redrawn. The topology, the part
choices and the control interface are unaffected, which is the point of separating them.

## Conditions for reopening

- If EXP-004 finds no analyser coverage at the chosen band, revisit the frequency, not
  the topology.
- If EXP-004 finds a single port analyser, the mutual coupling route closes, R2 loses
  its value, and the two board split has to be re-justified on the remaining grounds.
- If EXP-005 shows the detector path cannot support unattended runs, the unattended
  dataset fails and decision 0002 is superseded before this one is.
- If measured switch state repeatability is not below the measurement floor, replace
  the phase control approach rather than continuing, because the experiment is
  otherwise unfalsifiable.
- If the budget forces a reduction, take it from the neutral levers in section 6.1 of
  the architecture document, which free about 19 EUR without touching the
  architecture. **The phase bit count and the element count are not budget levers.**
  Reducing either is a supersession of this decision, or of decision 0002, and not a
  substitution. Section 8.1 of the architecture document states what two bit operation
  costs and what has to be recomputed if it is ever chosen.
- If sidelobe level becomes a target rather than an observation, fit the PE4312 and
  reopen the amplitude decision.
