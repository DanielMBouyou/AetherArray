# EXP-004 results

- Status: partial, five of nine observations complete, frequency inputs all passing
- Last reviewed: 2026-09-21

Plan and decision rule in `experiments/EXP-004-instrument-audit.md`.

## Result 1, 2026-09-19: no local evidence identifies the instruments

A negative result, recorded so that the search is not repeated. Every avenue that
could have identified the network analyser without walking to the bench was tried and
none carried information.

| Avenue | Method | Outcome |
| --- | --- | --- |
| Consolidated private inventory | read the instrument section | every field marked entirely unknown |
| Instrument and driver software | enumerate installed programs for the known vendor and interface names | none installed |
| Instrument control library | check whether the standard instrument control package is importable | absent |
| Historic USB attachment | read the operating system device enumeration records for the vendor identifiers of the mainstream instrument makers | no such vendor identifier has ever been enumerated on this machine |
| Instrument class devices | search the same records for the standard instrument class driver | none |
| Saved measurements | search the user profile for Touchstone files | none, other than the sample files shipped inside a library |

### What this rules out

The analyser has never been connected to this computer. That is consistent with the
inventory, and it means the remote interface, observation O9, is unproven as well as
the rest.

### What it does not rule out

An instrument that exists, works, and has simply never been plugged in. Nothing here
is evidence about the instrument itself, only about its absence from this machine.

### Consequence

The bench visit is unavoidable. It is also now short: the analysis in the experiment
document reduces the frequency decision to one reading, observation O2.

## Result 2, 2026-09-20: partial bench observations

Reported by the operator from a Rohde and Schwarz ZVL on the bench. These are panel
observations relayed to this record, not readings taken from a datasheet, and the
distinction is kept in the last column.

| N | Observation | Reading | Date | Against the expected value |
| --- | --- | --- | --- | --- |
| O1 | Manufacturer, model, serial | Rohde and Schwarz ZVL. **Exact model and serial not read** | 2026-09-20 | **partial.** The properties match the ZVL3, the 3 GHz member, but the identification is inferred from behaviour rather than read from the label |
| O2 | Maximum sweep frequency | 3 GHz | 2026-09-20 | **pass**, criterion was at or above 2500 MHz |
| O3 | Minimum sweep frequency | 9 kHz | 2026-09-20 | **pass**, criterion was at or below 100 MHz |
| O4 | Transmission measurement available | S21 available | 2026-09-20 | **pass** |
| O5 | Complex format available | complex and phase formats available | 2026-09-20 | **pass** |
| O6 | Source power | capability up to 0 dBm. **The level to be used has not been chosen or recorded** | 2026-09-20 | **partial.** The capability is inside the window of -25 to +8 dBm, and the 0 dBm ceiling sits 8 dB below the radiated limit, so the instrument cannot breach it |
| O7 | Calibration kit and connector type | ports are N female. **No calibration kit confirmed, no adapter confirmed** | 2026-09-20 | **partial, and the most consequential gap.** See `docs/hardware/measurement-bench.md` section 6 |
| O8 | Time domain or gating present | not verified | | **outstanding.** Record the option list verbatim from the version and options page; do not go looking for one designation, because the published mappings are unconfirmed. Not a gate |
| O9 | Remote interface | USB present on the instrument. **Enumeration on the computer not verified** | 2026-09-20 | **partial.** No instrument has ever enumerated on this computer, per result 1 |

Also observed: the system impedance is 50 ohm, which matches the design.

### What this settles

The three observations that decide the working frequency, O2, O4 and O5, all pass. A
3 GHz instrument with transmission and complex formats supports 2.44 GHz.

### What still prevents closure

| Item | Why it blocks | Effort |
| --- | --- | --- |
| O1 exact model and serial | the pre-committed procedure requires every reading to be checked against the datasheet of the exact model, and "a ZVL" does not select a datasheet | read the rear label |
| O7 calibration kit and adapters | without a kit and an N to 3.5 mm or N to SMA adapter there is no calibrated measurement at the board reference plane, whatever the frequency | look in the case |
| O6 the level actually used | it is a procedure parameter, and the conducted and radiated cases want different values | set it and write it down |
| O8 installed option list | decides the echo strategy for EXP-005 | one menu, the version and options page |
| O9 enumeration on the computer | decides whether EXP-014 can run unattended | plug the cable in |

Only the first is a gate on the frequency decision. The rest are gates on measuring
anything well.

No cell in this table is filled from a catalogue, a memory or a guess. A reading that
was not taken stays blank or is marked outstanding.
