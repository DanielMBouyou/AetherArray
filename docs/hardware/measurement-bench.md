# Measurement bench architecture

- Status: in progress, one instrument partly confirmed, the rest documented only
- Last reviewed: 2026-09-21

Which instrument performs which Rev A measurement, what each one is capable of
according to its manufacturer, and what has actually been seen.

## 1. Four classes of evidence, kept apart

The distinction matters more here than anywhere else in the repository, because an
instrument that is documented in an inventory and an instrument that is sitting on the
bench are not the same thing, and a measurement plan built on the first is a plan built
on nothing.

| Class | Meaning | How it is written below |
| --- | --- | --- |
| **Confirmed present** | somebody has stood in front of it and read the panel | `[observed]` with the date |
| **Documented historical** | listed in the laboratory inventory, presence today unknown | `[inventory]` |
| **Capability, manufacturer** | stated by the manufacturer for that model family | `[vendor]` |
| **Capability, secondary** | stated only by distributor or aggregator listings | `[listing]` |

A capability can be verified while the instrument is unconfirmed. That combination
means "if it is there, it can do this", and nothing more.

**The fourth class exists because of a real limitation.** The manufacturer datasheets
for these instruments could not be read here: the network analyser datasheet is a
scanned image, and the manufacturer product page for it is now a discontinued product
stub that no longer carries the option list. Anything marked `[listing]` therefore
rests on resellers repeating a specification, which is usually right and is not a
source this repository treats as established. Nothing in section 4 is allowed to
depend on a `[listing]` claim.

## 2. Instruments

### 2.1 The one with current evidence

A Rohde and Schwarz ZVL was observed on 2026-09-20. **The exact model and serial have
not been read**, so the identification rests on the observed properties matching one
member of the family.

| Observed property | Value | Consistent with |
| --- | --- | --- |
| System impedance | 50 ohm | the whole family |
| Frequency range | 9 kHz to 3 GHz | the 3 GHz member of the family |
| Port connectors | N female | the family |
| Transmission measurement | available | the family |
| Complex and phase formats | available | the family |
| Source capability | up to 0 dBm | the family |
| Remote interface | USB present | the family |

This instrument does **not** appear in the documented laboratory inventory. It is an
addition to it, or the inventory is out of date. Either way it is the only instrument
with any current evidence behind it, so the bench architecture below is built so that
it alone is sufficient.

### 2.2 Documented, presence not confirmed

| Instrument | Class | Role if present |
| --- | --- | --- |
| Agilent N9923A FieldFox RF vector network analyser | `[inventory]` | the independent cross check for every vector measurement |
| HP 8714C economy network analyser | `[inventory]` | a second, older cross check |
| Agilent N9000A CXA signal analyser | `[inventory]` | absolute power reference and harmonic work |
| HP 8562A spectrum analyser | `[inventory]` | second spectrum instrument |

## 3. Measurement matrix

Every cell carries its evidence class. References in `docs/references/bibliography.md`.

| Axis | The observed analyser | N9923A | 8714C | N9000A CXA | 8562A |
| --- | --- | --- | --- | --- | --- |
| Frequency range | 9 kHz to 3 GHz `[observed]` | 2 MHz to 4 GHz, 6 GHz variant exists `[vendor]` | 300 kHz to 3 GHz `[vendor]` | 9 kHz to 26.5 GHz, model dependent `[vendor]` | **9 kHz to 22 GHz** `[vendor]` |
| S-parameters | S21 `[observed]`; full two port `[listing]` | S11 and S21; **all four are option dependent, option 122, see below** `[vendor]` | transmission and reflection `[vendor]` | none, receiver only | none, receiver only |
| Phase and complex data | yes `[observed]` | yes, phase and Smith `[inventory]` | to verify | not applicable | not applicable |
| Dynamic range | up to 123 dB `[listing]` | above 100 dB vector, four independent receivers `[vendor]`; up to 90 dB for four parameters `[listing]` | above 100 dB narrowband `[listing]` | not applicable | not applicable |
| Source capability | **up to 0 dBm** `[observed]`; lower limit -50 dBm `[listing]` | to verify | **up to +16 dBm** `[listing]` | none | none |
| Calibration method | OSM, TOSM, one path two port `[listing]` | SOLT, and a built in quick calibration `[vendor]` | to verify | not applicable | not applicable |
| Connector standard | **N female** `[observed]` | 3.5 mm kits documented `[inventory]`, port family to verify | to verify | to verify | to verify |
| Remote and export | USB present `[observed]`; Ethernet standard and GPIB optional `[listing]` | S2P export over USB `[inventory]` | to verify | to verify | to verify |
| Time domain | **option dependent and unverified, see below** | distance to fault available `[listing]` | to verify | not applicable | not applicable |
| Safe input limit | **not read for any instrument** | not read | not read | not read | not read |

Three rows deserve comment.

**Source capability.** The observed instrument cannot exceed 0 dBm, and that was read
from the panel rather than inferred. Section 5 shows why it is a useful property rather
than a limitation. The 8714C can reach +16 dBm, which is above the radiated ceiling
this project must respect, so if it is ever used for a radiated measurement its output
has to be set deliberately rather than left where it was found.

**Option designations, now established against manufacturer sources.** Checked
2026-09-21, bibliography `[T1a]` and `[T2]`:

| Designation | Meaning | Source |
| --- | --- | --- |
| K1 | spectrum analysis | manufacturer option listing, and a manufacturer manual titled for this option `[vendor]` |
| K2 | distance to fault | manufacturer option listing `[vendor]` |
| K3 | time domain analysis | manufacturer option listing `[vendor]` |
| 122, handheld analyser | full two port S-parameters, adding S22 and S12 to the base S11 and S21, with full two port calibration | manufacturer options page and technical overview `[vendor]` |

The distributor listings turned out to be right. An earlier draft of this document
asserted the K3 mapping as a correction of fact, then withdrew the assertion for want
of a source; the mapping is now carried on a manufacturer source rather than on either.
The earlier doubt about option 122 came from reading a passage that mentions it
alongside an external generator measurement, which is a different sentence about the
same option, not a different meaning for it.

**What this does not establish, and the distinction is the whole point.** Knowing what
a designation means says nothing about **which options are installed on the unit on the
bench**. That is still unread, it is still `O8`, and `O8` still records the option list
**verbatim** rather than going looking for a designation it expects to find. The
identification of the unit is still an inference from behaviour, so the manual to read
each entry against is the manual for whatever model `O1` returns, not the one assumed
here.

**Safe input limits are unread for every instrument.** Our own levels are far too low
to threaten anything, but the row says unread rather than safe.

## 4. Instrument assigned to each task

Primary is the instrument the measurement is designed around. Cross check is an
independent route to the same number, and it is marked conditional wherever the
instrument is `[inventory]` rather than confirmed.

| Task | Measurement | Primary | Independent cross check |
| --- | --- | --- | --- |
| EXP-004, instrument audit | panel readings and option list | the analyser itself | manufacturer datasheet for the exact model |
| EXP-005, repeatability | repeated transmission measurement and repeated detector reading | the observed analyser, S21 | **the on board AD8318 path**, which is genuinely independent: different receiver, different physics, already in the design |
| Switched line phase verification, 45, 90 and 180 degree bits | S21 phase against commanded code word | the observed analyser, S21 phase | N9923A, conditional on presence and on option 122 being installed |
| Channel insertion loss | S21 magnitude per channel and per code word | the observed analyser | 8714C, conditional |
| Wilkinson divider | S21 balance between arms, S11, port to port isolation | the observed analyser | N9923A, conditional on presence and option |
| Antenna reflection | S11 at each element port | the observed analyser | N9923A, conditional |
| Mutual coupling, element pairs | S21 between two element connectors, others terminated | the observed analyser | N9923A, conditional |
| Complex per element labels for ML-B | S21 from the common port to element port n, one channel enabled | **the observed analyser, with data export over the remote interface** | repeat measurement after reconnection, which is the check that matters for this number |
| AD8318 validation | detector output voltage against a known input power | the observed analyser as a calibrated source, stepped | N9000A CXA or 8562A as an absolute power reference, conditional |
| Spectrum and harmonics | harmonic content of the source, switch nonlinearity | N9000A CXA, conditional | 8562A, conditional, or the observed analyser if a spectrum option turns out to be installed |

The pattern to notice: **every critical measurement has the observed analyser as primary, and the
only cross checks that do not depend on an unconfirmed instrument are the on board
detector and repetition.** That is a thin position, and it is the honest one.

## 5. What the 0 dBm source ceiling settles

EXP-004 derived a regulatory ceiling on radiated source power: with a 2 dBi probe, the
10 mW equivalent isotropic radiated power limit of band 57a caps the source at about
+8 dBm.

The observed maximum output is 0 dBm, read from the panel, which is 8 dB below that
ceiling.

**So compliance is guaranteed by the instrument rather than by the operator
remembering.** That closes a risk rather than managing it. It does not hold for the
8714C at +16 dBm, which is the reason that row is called out above.

For conducted work the opposite end matters. Driving the board directly at 0 dBm, with
about 4 dB of chain loss and no path loss, puts roughly -4 dBm into the detector, near
the top of its useful range. A conducted source setting around -10 dBm is the sensible
default, and that is what observation O6 should record.

## 6. The connector chain, and the most likely practical blocker

| Element | Interface |
| --- | --- |
| ZVL ports | N female, `[observed]` |
| Rev A board | SMA, `decisions/0003-rev-a-rf-architecture.md` |
| Calibration kits named in the inventory | 3.5 mm, 85033D or 85033E, and 85052D |

Those three do not join up on their own. The documented kits are 3.5 mm and belong to
the handheld analyser, not to the ZVL.

A chain that **would** work, **if and only if** the parts turn out to exist, is: the
analyser's N female port, an N male to 3.5 mm female adapter, then calibration with a
3.5 mm kit **at the adapter output plane**, then the board. It would work because
3.5 mm and SMA are mechanically compatible, so a 3.5 mm kit defines a reference plane
an SMA board can be connected to, at a small accuracy cost.

**This is a proposal, not a plan.** Every element of it is unconfirmed: no calibration
kit of any connector family has been seen, no adapter has been seen, and the 3.5 mm
kits named in the inventory belong to an instrument whose presence is itself
unconfirmed. Nothing may be ordered, scheduled or promised on the strength of this
paragraph until observation O7 says what is physically in the case.

What is missing is the adapters, and confirmation that any calibration kit is present
at all. **This, rather than the frequency, is the most likely thing to stop a real
measurement.** It falls inside observation O7 and needs no new observation to cover it.

## 7. What this does not settle

- No instrument other than the ZVL has been confirmed to exist.
- The ZVL option list has not been read, so time domain, spectrum analysis and the
  reference oscillator are all unknown.
- No safe input limit has been read from any datasheet.
- Nothing here fixes a transmission line length, an antenna dimension or a board
  layout, and nothing here is permitted to.
