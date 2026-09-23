# Control architecture: the external DE1-SoC controller

- Status: specified, schematic re-capture required, no gateware written
- Last reviewed: 2026-09-23

Rev A is driven by a DE1-SoC board sitting beside the radio frequency board, not by
the microcontroller assumed in decision 0003. This document defines the partition, the
beam state interface, the acquisition path and the connector the radio frequency board
must carry. Decision recorded in `decisions/0005-de1-soc-controller.md`.

**The radio frequency topology does not change.** Nothing here touches the divider, the
switched line chain, the element ports or the detector. What changes is what drives
them and what records the result.

---

## 1. Why a controller change was worth making

`docs/hardware/rev-a-requirements.md` section 6 previously answered uncertainty I10 by
saying this project has no need of an FPGA. That answer was correct for the question
it was asked, which was whether beamforming needs one. It was wrong about a different
question, which is what the **measurement** needs.

The reason is the one the project has been circling since decision 0002. The central
claim is about drift measured close to the noise floor, so anything that adds scatter
correlated with the measurement sequence is indistinguishable from a physical result.

| Requirement | Why a fabric implementation is different in kind |
| --- | --- |
| The delay between applying a beam state and sampling the detector must be identical every time | on a general purpose controller this delay is subject to interrupts, scheduling and the host link, and the jitter enters the data as scatter |
| All sixteen control bits must change at one instant | a fabric register updates on one clock edge; a processor writes ports in sequence |
| Every record must carry a timestamp from the same clock as the trigger | otherwise the time axis of the drift experiment is assembled from two clocks |
| The sequence must run unattended for hours | decision 0002's figure of merit is unattended calibrations per hour |
| The control lines must be quiet while the detector is sampled | sixteen lines switching beside a receive chain inject noise **correlated with the beam state**, which is the worst possible kind here |

The last row is the one that decides it. Noise that is random degrades a measurement.
Noise that is correlated with the commanded state imitates a calibration coefficient.

---

## 2. Partition

```
 PC (optional)          DE1-SoC HPS                 DE1-SoC FPGA fabric         RF board
 ------------           -----------                 -------------------         --------
 heavy inference   <->  orchestration          <->  beam state register    -->  16 data + strobe
 training              storage, session log         sequencer                   registered buffer
 analysis, plots       posterior update             trigger generator           switches
                       active selection             timestamp counter
                                                    SPI master             <--  on board converter
                                                    I2C master             <->  temperature sensors
                                                    record FIFO
```

| Layer | Owns | Does not own |
| --- | --- | --- |
| **FPGA fabric** | deterministic application of a beam state, sequencing, trigger generation, timestamps, the converter and sensor interfaces, buffering records | any floating point, any inference, any storage |
| **HPS**, the processor on the same device | loading sequences, draining records to disk, session metadata, the posterior update, choosing the next measurement | anything with a hard timing requirement |
| **PC**, optional | training the drift prior, analysis, figures | anything the experiment depends on at run time |

The split is a timing split, not a capability split. Everything with a deadline is in
fabric. Everything probabilistic is above it.

---

## 3. The beam state interface

### 3.1 The word

Sixteen bits, one per controllable switch input, in a fixed order.

Bit $b$ of the word carries field $f$ of channel $c$, with

```math
b = 4c + f, \qquad c \in \{0,1,2,3\}, \qquad f \in \{0,1,2,3\}
```

and the field index $f$ meaning enable, 45, 90 and 180 in that order. Written out:

| Bit | 0 | 1 | 2 | 3 | 4 | ... | 15 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Channel | 0 | 0 | 0 | 0 | 1 | ... | 3 |
| Field | enable | 45 | 90 | 180 | enable | ... | 180 |

**Logical polarity is defined here; electrical polarity is not.** A bit set to one means
the channel is enabled, or that bit's delay arm is selected. Whether that corresponds to
a high or a low at the switch control pin depends on the PE4259-63 single pin truth
table, which has not been read. That mapping is **one inversion constant per field in
gateware**, applied between this word and the output register, and it is set once the
truth table is available. Nothing else in the design depends on it.

The monitor path select, `MON_SEL` in the captured schematic, is a seventeenth line
and is deliberately **not** part of the beam state word. It selects which instrument
sees the common port and does not change between measurements within a sweep.

### 3.2 Synchronous application

The word is applied at one instant, not bit by bit.

1. The HPS, or the fabric sequencer, writes the sixteen bits into a fabric register.
2. The fabric drives the sixteen data lines and holds them.
3. After the lines have settled, the fabric pulses one `STROBE` line.
4. A registered buffer **on the radio frequency board** captures all sixteen bits on
   that single edge and presents them to the switches.

Step 4 is what makes the application synchronous where it matters. The cable carries
skew; the buffer removes it, because every output changes on one clock edge at the
board rather than on sixteen arrivals.

### 3.3 Why a buffer is required, and what it does not settle

An earlier version of this section said the buffer "removes the question" of electrical
compatibility. **That was wrong, and the error is worth naming because it is an easy
one.** Buffering answers one electrical question and leaves a different one wide open.

**What the buffer does settle.** The DE1-SoC expansion header pins are 3.3 V, connected
directly to the Cyclone V device, with 3.3 V protection diodes, bibliography T6. A
buffer powered from the board 3V3 rail, the same rail as the switch supply pins, cannot
drive its outputs above that rail. So the switch control input is never presented with a
voltage above its own supply, whatever the controller does. That is the **overvoltage**
question, and a common rail buffer does close it by construction.

It also settles three things that have nothing to do with levels: edges are restored
where the cable enters the board, cable skew is removed because all sixteen outputs
change on one clock edge at the board, and the controller is isolated from the radio
frequency board.

**What the buffer does not settle.** Whether the switch actually *reads* the buffer's
output as a logic one or a logic zero. That needs two numbers on each side:

| Needed | Status |
| --- | --- |
| PE4259-63 control input high threshold and low threshold at the chosen supply | **not obtained.** The vendor datasheet is a scanned image, bibliography V1 |
| Guaranteed output high and output low of the selected buffer, at the design load and over temperature | **not obtained, because no buffer has been selected** |

Both columns are empty, so **no claim of logic level compatibility is made here, buffered
or direct.** Putting a buffer in the path changes which part has to be checked; it does
not remove the check. See the open item in section 8.

**The controller is external.** Sixteen lines crossing a cable into a board carrying a
2.44 GHz receive chain need defined edges and a defined ground reference at the point
of use. A registered buffer at the board edge provides both.

| Requirement on the buffer | Reason |
| --- | --- |
| Registered, not transparent, clocked by `STROBE` | synchronous application, immune to cable skew |
| Supplied from the board 3V3 rail | output levels referenced to the switch supply |
| Two 8 bit devices, or one 16 bit device | sixteen lines |
| Sited at the connector, before the switches | edges restored where they enter the board |

Part selection is a follow-up, not made here.

---

## 4. Acquisition

**The fabric does not sample an analogue voltage.** It cannot. Every analogue quantity
reaches it through a converter.

### 4.1 The detector path

| Item | Specification |
| --- | --- |
| Source | AD8318 output, about 0.4 V to 2.2 V for the usable range, slope $-25$ mV/dB |
| Converter | a serial converter **on the radio frequency board**, beside the detector |
| Resolution required | at least 14 effective bits over a 2 V span, so that one step is below 0.01 dB. At $-25$ mV/dB, 0.1 dB is 2.5 mV |
| Interface | serial, four lines, mastered by the fabric |
| Trigger | the fabric asserts conversion after the settling delay, and timestamps it |

**Why the converter is placed on the radio frequency board, and on what strength of
evidence.** This is a **precaution, not a measured necessity**, and the distinction is
recorded because the two are easy to blur.

The DE1-SoC already carries an eight channel twelve bit converter with a 0 V to 4.096 V
input range, bibliography T6, and using it would cost nothing. It would carry a single
ended analogue signal, where 0.1 dB is 2.5 mV, along a ribbon cable beside sixteen
digital lines, with the two boards sharing a ground only through that cable.

| Claim | Status |
| --- | --- |
| A ribbon path can pick up interference from adjacent switching lines and from a shared ground return | mechanism, uncontroversial |
| Such an error would be **correlated with the commanded state**, and a state correlated error imitates a calibration coefficient rather than looking like noise | reasoning, and it is why the consequence is severe rather than merely untidy |
| The magnitude of that pickup on this cable, with this board, exceeds what the drift experiment can tolerate | **not measured.** This is the assumption |

So the argument for the local converter is asymmetric cost, not demonstrated failure.
Fitting it costs a few euro and a little board area. Omitting it and being wrong costs
a board revision, and the symptom would be a plausible looking calibration coefficient
rather than an obvious fault. On that asymmetry the local converter is preferred.

**The onboard converter is kept as an independent path, not discarded.** It samples a
different chain from a different ground reference, which is exactly what makes a
disagreement between the two informative. It also serves slow quantities such as supply
monitoring.

**EXP-005 turns this from an argument into a measurement**, and it can do so before the
board exists: feed one detector output to a local converter and to the DE1-SoC converter
through the intended ribbon, first with the control lines idle and then with them
toggling, and compare. If the two paths agree to well inside the repeatability floor,
the local converter is a precaution that was not needed and the requirement is demoted.
That comparison is written into EXP-005.

### 4.2 The temperature path

The two MCP9808 sensors are digital and need no converter. The fabric carries an I2C
master; the sensors sit at addresses 0x18 and 0x19 as captured. A reading is taken with
each measurement record rather than on a separate schedule, so that every sample has its
own temperature rather than an interpolated one.

The AD8318 die temperature output is analogue and goes to a second converter channel.

---

## 5. Sequencer, trigger and timestamps

The fabric executes a sequence without host involvement. One entry is:

| Field | Meaning |
| --- | --- |
| beam state word | the sixteen bits to apply |
| settling delay | time from `STROBE` to conversion trigger |
| sample count | conversions to average at this state |
| repeat count | times to revisit this state within the sweep |

Three guarantees the fabric provides, and a processor does not:

1. **The settling delay is exact.** Same number of clock cycles every time, recorded in
   the record rather than assumed.
2. **The control lines are static during the sample window.** No line changes between
   the strobe and the last conversion of that entry. This is a hard rule in the
   sequencer, not a convention.
3. **One clock timestamps everything.** A free running counter timestamps the strobe
   and each conversion, so the time axis of the drift experiment comes from one source.

Wall clock time is attached once per session by the HPS and related to the counter, so
that long term drift can be plotted against real time without the counter having to be
correct in absolute terms.

### 5.1 Semantics, pinned down

Written at this level of detail because these are the points where a later
implementation would otherwise have to guess, and two implementations guessing
differently would produce datasets that cannot be pooled.

| Item | Definition |
| --- | --- |
| Strobe edge | the **rising** edge captures. One pulse per beam state, never repeated for the same state |
| Data setup and hold | the sixteen data lines are stable for a setup time before the strobe edge and a hold time after it. Both values follow from the selected buffer and the cable, so they are fixed when H4 closes, not now |
| Settling interval | counted in sequencer clock cycles **from the strobe rising edge at the controller**, not at the board. Cable and buffer delay sit inside the interval on purpose, so the interval is measured from the one event that is also timestamped |
| Trigger | asserted by the sequencer when the settling interval expires |
| Timestamp instant | taken at the **trigger edge**, not at the converter's internal sampling instant. The converter's aperture delay is a constant of the chosen part, recorded once per campaign rather than per sample |
| Counter | free running, monotonic within a session. If it can roll over inside the longest planned session, the record carries a rollover count; a wrapped timestamp with no rollover field is not acceptable |
| Quiet window | from the strobe rising edge to the end of the last conversion of that sequencer entry, **no control line changes and no I2C traffic occurs**. Temperature reads are scheduled outside it |

The I2C clause matters as much as the control line clause. An I2C transaction is
switching activity on two more lines in the same cable, and scheduling it during a
conversion would reintroduce exactly the interference the quiet window exists to avoid.

### 5.2 What the read back actually proves

The record carries a read back beam state word. It is worth being exact about what that
detects, because the obvious reading is too generous.

A registered buffer of the ordinary octal flip flop kind has no read back path. The
word that can be read is therefore **the controller's own output register**, which
proves the gateware wrote what the sequencer intended. It does **not** prove that the
cable, the connector, the buffer or the switch received it.

| Fault | Detected by reading the controller register |
| --- | --- |
| Sequencer or software wrote the wrong word | **yes** |
| Broken conductor, bad connector contact, failed buffer, unpowered buffer | **no** |

Detecting the second class needs a return path from the buffer outputs back to the
controller, which the interface in section 7 does not currently carry. That is a
deliberate omission for now and not an oversight: it would cost sixteen more lines, and
the same faults are caught much more cheaply by a bring up check that walks a single bit
through all sixteen positions and watches the radio frequency response. The field name in
the record schema is kept as is, and this paragraph is what it means.

---

## 6. Minimum record

Every measurement writes one record. A field that was not captured is absent, not
defaulted.

| Field | Source | Why it is not optional |
| --- | --- | --- |
| session identifier | HPS | groups a sweep |
| sequence index | fabric | ordering within the sweep |
| beam state word, commanded | fabric register | the input to the forward model |
| beam state word, read back | buffer read back path, if fitted, else the register | detects a control fault rather than absorbing it into the data |
| strobe timestamp | fabric counter | start of the settling window |
| conversion timestamp | fabric counter | the measurement instant |
| settling delay applied | sequencer entry | makes the timing reproducible from the record alone |
| raw converter counts | converter | the measurement before any scaling |
| converter reference and channel | fabric | a reference change is otherwise invisible |
| detector temperature | MCP9808 at 0x19 | the AD8318 stability figure is corrected against it |
| phase network temperature | MCP9808 at 0x18 | separates array drift from detector drift |
| die temperature | AD8318 TEMP channel | third, independent temperature |
| gateware and software version | HPS | a timing change between sessions is otherwise silent |
| connector handling flag | operator, per session | uncertainty I14 depends on it |
| instrument state, if the analyser was used | HPS | source power, intermediate frequency bandwidth, calibration identifier |

These are the fields the learning track in section 8 consumes. They are specified here
rather than in the experiment because a record schema that changes between sessions
destroys the dataset.

---

## 7. What the radio frequency board must expose

The connector is defined here; the schematic that carries it is not yet updated.

| Group | Lines | Note |
| --- | --- | --- |
| Beam state data | 16 | into the registered buffer |
| Strobe | 1 | buffer clock |
| Monitor path select | 1 | not part of the beam state word |
| Converter serial interface | 4 | clock, data in, data out, chip select |
| Temperature I2C | 2 | clock and data, pull ups on the board |
| 5 V in | 1 | detector supply |
| 3V3 in | 1 | switches, buffer, sensors |
| Ground | several, interleaved | return for sixteen switching lines beside a receive chain |

That is about 26 signal lines plus grounds. A 2 by 20 ribbon connector carries it with
grounds interleaved, which the current 2 by 13 does not.

**Consequence, recorded and not acted on here.** The captured schematic must be
re-captured to match: the interface symbol changes from a microcontroller header to this
connector, the two registered buffers appear between it and the switches, the analogue
return pins become a serial converter interface, and the converter is added beside the
detector. That is a schematic change with no radio frequency consequence, and it is a
follow-up task rather than part of this review.

---

## 8. Open items

| Item | Why it is open |
| --- | --- |
| **H1, logic level compatibility** | **blocks board release.** See below |
| H2, expansion header supply capability | the header carries 5 V and 3V3, bibliography T6, but no current limit was obtained. If it cannot source about 70 mA, the board takes a separate supply and the grounding question in H5 grows |
| H3, converter part selection | a requirement is stated in section 4.1, no part is chosen |
| H4, buffer part selection | requirements in section 3.3, no part is chosen. H1 cannot close until this does |
| H5, ground strategy between the two boards | a long ribbon between a digital board and a receive chain is a loop; this needs a decision before layout |

### H1, stated as an acceptance test

Logic level compatibility between the control path and the switch control input is
**unresolved**, and the buffer does not resolve it. It closes when all four of these
exist, with their sources and conditions recorded:

1. PE4259-63 control input high threshold, minimum, at the supply the board uses.
2. PE4259-63 control input low threshold, maximum, at the same supply.
3. Selected buffer guaranteed output high, minimum, at the design load and over the
   working temperature range.
4. Selected buffer guaranteed output low, maximum, at the same conditions.

Acceptance is item 3 above item 1 with margin, and item 4 below item 2 with margin. The
margin is stated when the numbers are.

Items 1 and 2 need a person with the datasheet open, because the file is a scanned
image and could not be read here. **If they cannot be obtained at all**, the fallback is
a level translator whose output levels are specified against a named input standard,
plus a bench measurement of the actual switching threshold on a sample device. That
fallback costs a part and an afternoon, and it is preferable to releasing a board on an
assumption.

**This is a gate on board release, not on the architecture.** Nothing above depends on
the answer; only the choice of part in section 3.3 does.
