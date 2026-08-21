# Proposed hardware to buy

- Status: proposal, nothing ordered, blocked on the measurement audit
- Last reviewed: 2026-08-21

The lab already owns the instruments, the FPGA boards, the microcontrollers, the
PCs and the simulation software. None of that is bought again. This document covers
only what the project needs and does not have.

Each candidate is judged on seven points: the function required, candidate parts,
estimated price, compatibility with what we own, why it is necessary, reuse
potential, and the risk of choosing too early.

---

## The reasoning behind buying anything at all

The simulation half of this project needs nothing: a simulator with injected defects
answers the algorithmic questions, and thanks to the available electromagnetic tools
the injected coupling can even come from physics rather than from a guess.

But the whole point of the project is the gap between that simulation and a real
array. Nobody needs another paper showing that least squares recovers coefficients
you injected yourself. The value is in showing what happens when the cables are
slightly different lengths, the connectors are tightened by hand and the room
reflects. That requires an array.

The purchase is therefore the array itself, and the minimum needed to measure it.

---

## Function 1: a real array with controllable phase

**Why it is necessary.** Without it, there is nothing to calibrate.

**Candidates for phase control.**

| Option | Principle | Resolution | Estimated price for 4 channels | Risk |
| --- | --- | --- | --- | --- |
| Switched line phase shifter using RF switches | select between two path lengths per bit | discrete, for example 90 degree steps with 2 bits | around 15 to 25 EUR of switches | low, and the quantisation error becomes a study subject in itself |
| Analogue phase shifter integrated circuit | continuous control | continuous | often 20 EUR or more per channel | high, cost grows fast with channel count |
| Varactor based phase shifter | continuous, built from passives | continuous but non linear | around 10 EUR | medium, needs careful characterisation |
| Digital beamforming | phase applied in the digital domain | excellent | requires coherent converters we do not have | very high |

**Proposal.** Switched line phase shifting with small RF switches. It is the
cheapest route, it is fully understandable, and the quantisation it introduces is
itself worth studying: with 90 degree steps the worst case phase error is 45
degrees, which visibly degrades the pattern. Measuring that degradation and
comparing it against theory is a good experiment.

**Reusable later?** The switches, yes. The board, no.

**Risk of choosing too early.** Medium, because the parts depend on the working
frequency, which depends on the instrument audit. Blocked until then.

## Function 2: the antennas and the feed network

**Why it is necessary.** Four antennas that are as identical as possible, and a way
to split one source into four channels.

**A point worth stating**: reproducibility between elements matters more than the
performance of any one element. An array of four mediocre but identical antennas
calibrates better than four good but different ones.

**Candidates.** Printed antennas on the same board as the feed network. A four way
splitter can be printed on the board too, which costs nothing beyond board area.

**Proposal.** One printed board carrying the four antennas, the splitter and the
phase shifters. Fabrication cost shared with the RF modelling project, around 10 to
15 EUR as this project's share.

## Function 3: measure what the array actually does

**Why it is necessary.** A pattern measured by hand at five points is an anecdote.

**Candidates.**

| Option | Estimated price | Note |
| --- | --- | --- |
| RF power detector breakout | 10 to 15 EUR | gives a cheap scalar receiver, usable without tying up the network analyser |
| Stepper motor, driver and mechanical parts | 12 to 18 EUR | the angular positioner, driven by an STM32 we already own |
| SMA connectors and cables | 15 to 20 EUR | shared with the RF modelling project |

**Proposal.** All three. The positioner in particular is what turns pattern
measurement from a manual chore into an automated campaign, and it serves the other
RF project too.

**Reusable later?** The positioner and the connectors, heavily.

---

## Draft bill of materials

| Item | Quantity | Unit | Total |
| --- | --- | --- | --- |
| RF switches for switched line phase shifting | 8 | around 2.5 EUR | around 20 EUR |
| Board fabrication share, antennas plus feed network | 1 | around 12 EUR | around 12 EUR |
| RF passives, matching and bias components | 1 set | around 8 EUR | around 8 EUR |
| Stepper motor, driver and mechanical hardware | 1 set | around 15 EUR | around 15 EUR |
| RF power detector breakout | 1 | around 12 EUR | around 12 EUR |
| **Total** | | | **around 67 EUR** |

SMA connectors and cables do not appear here: under the lab accounting rule they are
bought once by whichever RF project needs them first, and counted there. If this
project buys them first, they move into this list and something else moves out.

Prices are indicative and must be re-checked before ordering.

## What has to be settled before ordering

- [ ] Measurement audit done, so we know whether radiated measurement is viable at
      all
- [ ] Decision made between the radio frequency and the acoustic route, since it
      changes every line above
- [ ] Working frequency chosen, since it determines the switches, the antenna
      geometry and the board material
- [ ] Element count decided, since it scales the switch count directly
- [ ] Board order grouped with the RF modelling project

Until the first two boxes are ticked, ordering RF parts would be guessing.
