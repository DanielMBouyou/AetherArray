# EXP-004 results

- Status: partial, four of nine complete, four partial and one not taken; the frequency question inside it is closed
- Last reviewed: 2026-09-28

The plan and its decision rule are in `experiments/EXP-004-instrument-audit.md`. The
visit that finishes it has a step by step runbook, SCH-001, in `docs/runbooks/`.

## Result 1, 2026-09-19: no local evidence identifies the instruments

This is a negative result, written down so nobody repeats the search. We tried every
way of identifying the network analyser without walking over to the bench, and none of
them told us anything.

| Avenue | Method | Outcome |
| --- | --- | --- |
| Consolidated private inventory | read the instrument section | every field marked entirely unknown |
| Instrument and driver software | enumerate installed programs for the known vendor and interface names | none installed |
| Instrument control library | check whether the standard instrument control package is importable | absent |
| Historic USB attachment | read the operating system device enumeration records for the vendor identifiers of the mainstream instrument makers | no such vendor identifier has ever been enumerated on this machine |
| Instrument class devices | search the same records for the standard instrument class driver | none |
| Saved measurements | search the user profile for Touchstone files | none, other than the sample files shipped inside a library |

### What this rules out

The analyser has never been plugged into this computer. That fits the inventory, and
it means the remote interface, reading O9, is unproven like everything else.

### What it does not rule out

An instrument that exists, works, and just hasn't ever been plugged in. None of this
says anything about the instrument itself. It only says it has never met this machine.

### Consequence

The bench visit can't be avoided. It's short now, though: the analysis in the
experiment document boils the frequency decision down to one reading, O2.

## Result 2, 2026-09-20: partial bench observations

Reported by the operator, from a Rohde and Schwarz ZVL on the bench. These are what the
panel showed, passed on to this record. They aren't figures from a datasheet, and the
last column keeps that difference visible.

| N | Observation | Reading | Date | Against the expected value |
| --- | --- | --- | --- | --- |
| O1 | Manufacturer, model, serial | Rohde and Schwarz ZVL. **Exact model and serial not read** | 2026-09-20 | **partial.** The properties match the ZVL3, the 3 GHz member, but the identification is inferred from behaviour rather than read from the label |
| O2 | Maximum sweep frequency | 3 GHz | 2026-09-20 | **pass**, criterion was at or above 2500 MHz |
| O3 | Minimum sweep frequency | 9 kHz | 2026-09-20 | **pass**, criterion was at or below 100 MHz |
| O4 | Transmission measurement available | S21 available | 2026-09-20 | **pass** |
| O5 | Complex format available | complex and phase formats available | 2026-09-20 | **pass** |
| O6 | Source power | capability up to 0 dBm. **The level to be used has not been chosen or recorded** | 2026-09-20 | **partial.** The capability is inside the window of -25 to +8 dBm, and the 0 dBm ceiling sits 8 dB below the radiated limit, so the instrument cannot breach it |
| O7 | Calibration kit and connector type | ports are N female. **No calibration kit confirmed, no adapter confirmed** | 2026-09-20 | **partial, and the most consequential gap.** See `docs/hardware/measurement-bench.md` section 6 |
| O8 | Time domain or gating present | not verified | not taken | **outstanding.** Record the option list verbatim from the version and options page. What the designations mean is settled, bibliography `[T1a]`; which are installed is not. Not a gate |
| O9 | Remote interface | USB present on the instrument. **Enumeration on the computer not verified** | 2026-09-20 | **partial.** No instrument has ever enumerated on this computer, per result 1 |

Also seen: the system impedance is 50 ohm, which matches the design.

### What this settles

The three readings that decide the working frequency, O2, O4 and O5, all pass. A 3 GHz
instrument with transmission and complex formats handles 2.44 GHz, and decision 0004
fixed the frequency there on 2026-09-23.

It also closes gate G1. Phase can be measured, so the orthogonal coding baseline B5 is
available, and the per element complex label that supervises the learned drift prior
can be obtained as planned. Decision 0002 doesn't reopen.

### What still prevents closure of the experiment

Decision 0004 reclassified these on 2026-09-23, when it fixed the frequency from what
the instrument was seen to do rather than from its exact model. **None of them blocks
the RF design any more.**

| Item | What it blocks now | Effort |
| --- | --- | --- |
| O1 exact model and serial | provenance, and the key to every accuracy specification. **The one reading that could still overturn the frequency**, if the model proves to be specified below 2.44 GHz | read the rear label |
| O7 calibration kit and adapters | **calibrated hardware validation only.** Not simulation, not schematic work, not layout | look in the case |
| O6 the level actually used | a procedure parameter. The observed 0 dBm ceiling already guarantees the radiated limit cannot be breached | set it and write it down |
| O8 installed option list, copied verbatim | the echo strategy for EXP-005. Bench capability, not an architecture gate | one menu, the version and options page |
| O9 enumeration on the computer | unattended running in EXP-014. Automation, not an architecture gate | plug the cable in |

The experiment closes once all nine are recorded. The frequency question inside it is
already closed.

No cell in this table comes from a catalogue, a memory or a guess. A reading that
wasn't taken stays blank or is marked outstanding.
