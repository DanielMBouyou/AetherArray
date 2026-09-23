# 0004. The working frequency is 2.44 GHz

- Status: accepted
- Date: 2026-09-23
- Scope: Rev A radio frequency dimensioning, the simulation track, and every measurement that depends on the band

## Question

What is Rev A's working frequency, and what class of evidence is sufficient to fix it?

The second half of that question is the one that actually needed settling.

## Context

EXP-004 established that exactly one licence exempt band below the component ceiling
permits a continuous radiated carrier: band 57a, 2400 to 2483.5 MHz, at 10 mW
equivalent isotropic radiated power with no duty cycle restriction, bibliography R1.
The only open input was whether the available analyser could reach it.

On 2026-09-20 an analyser was observed on the bench and demonstrated, directly:
9 kHz to 3 GHz coverage, an S21 measurement, complex and phase display, 50 ohm ports,
and source capability up to 0 dBm.

The earlier closure logic then blocked the decision anyway, on the grounds that the
exact model had not been read and the procedure required each reading to be checked
against the datasheet of that model. **That reasoning was wrong, and this decision
corrects it.** A datasheet is evidence about what a manufacturer specifies for a model
family. A bench observation is evidence about the unit in the room. For the question
"can this instrument reach 2.44 GHz and measure a complex S21", the observation is the
stronger of the two, and the datasheet adds nothing that would change the answer.

The datasheet governs a different question: how *well* it measures. That question
belongs to validation, not to dimensioning.

## Options considered

### Option A: freeze on the observed capability

Fix the frequency now, from what the instrument was seen to do.

Upside: unblocks every dimensioning task, and rests on the strongest available
evidence for the question being asked. Downside: accuracy at 2.44 GHz stays unknown
until the model and the calibration hardware are identified.

### Option B: wait for the exact model

Keep the frequency open until the rear label is read and the datasheet checked.

Upside: provenance complete before anything downstream moves. Downside: the datasheet
cannot contradict a direct observation of coverage, so the wait buys no information
relevant to the decision. It holds the whole radio frequency design behind an
administrative step.

### Option C: wait for the model and for the calibration hardware

Also require observation O7 to establish a calibrated reference plane.

Upside: nothing is dimensioned before it can be validated. Downside: conflates two
independent things. A calibrated reference plane is needed to *measure* a board, not
to *design* one, and the simulation track needs no instrument at all.

## Comparison

| Criterion | A | B | C |
| --- | --- | --- | --- |
| Rests on the strongest evidence for the question asked | **yes** | no, it substitutes a weaker proxy | no |
| Unblocks simulation, schematic and layout dimensioning | **yes** | no | no |
| Risk of the answer being wrong | low, see limitations | low | low |
| Cost if wrong | redo line lengths and antenna geometry, no parts bought | none | none |
| Holds design behind an unrelated step | no | yes | yes, twice |

## Evidence

Measured bench facts and model specific specifications are separated below, because
the decision uses only the first column.

| Observed directly on the instrument, 2026-09-20 | Value |
| --- | --- |
| Frequency coverage | 9 kHz to 3 GHz |
| Transmission measurement | S21 available |
| Complex data | complex and phase formats available |
| System impedance | 50 ohm |
| Source capability | up to 0 dBm |
| Port connectors | N female |
| Remote interface | USB present |

| Model specific and still unknown | Consequence |
| --- | --- |
| Exact model and serial, observation O1 | no reading has been checked against a datasheet; this is provenance work |
| Specified accuracy, directivity and dynamic range at 2.44 GHz | affects measurement quality, not feasibility |
| Whether the observed 3 GHz is a specified limit or merely the highest value the panel accepts | see limitations |
| Installed options, observation O8 | affects the echo strategy, not the band |
| Calibration hardware present, observation O7 | blocks calibrated hardware validation, not design |

Other evidence already in the repository:

- Regulatory: band 57a carries no duty cycle restriction at 10 mW e.i.r.p.,
  bibliography R1. Every sub-band from 863 to 870 MHz is duty cycle limited, which is
  why there is no alternative.
- Component: the PE4259-63 covers 10 MHz to 3000 MHz, bibliography V1, so 2.44 GHz
  sits inside it. The AD8318 covers 1 MHz to 8 GHz, bibliography V6.
- Link budget, EXP-004: at the observed 0 dBm source ceiling the radiated level is
  about +2 dBm e.i.r.p. with a 2 dBi probe, which is 8 dB below the legal limit, and
  the sum port sees about -29.8 dBm radiated or about -4 dBm conducted. Both sit inside
  the detector range.

**No existing project requirement contradicts any of this.** That was checked against
the component ceilings, the regulatory table, gate G1 and the link budget.

## Decision

**The working frequency is fixed at $f_0 = 2.44$ GHz, in band 57a, 2400 to
2483.5 MHz.**

It is fixed on the observed capability of the instrument on the bench. Identification
of the exact model is recorded as outstanding provenance work and is **not** a
prerequisite for radio frequency dimensioning.

The closure logic of EXP-004 is amended accordingly: for a question of feasibility,
direct observation of the instrument takes precedence over model identification.

## Consequences

- **Gate G1 passes.** Phase is measurable, so the orthogonal coding baseline B5 is
  available and the per element complex label that supervises the learned drift prior
  can be obtained as designed. Decision 0002 does not reopen.
- The free space quantities that follow from $f_0$ alone are now determined, and were
  already published in EXP-004: a wavelength of 122.9 mm, half wavelength element
  spacing of 61.4 mm, an aperture of 184 mm across the element centres, and a far field
  distance of 0.55 m.
- **Printed line lengths remain blocked, but on a different thing.** They need the
  guided wavelength, which needs the stack-up. The frequency is no longer the blocker.
  `hardware/rev-a/layout-constraints.md` carries the change.
- The simulation track can now be run at a definite frequency, including the full wave
  coupling extraction of EXP-011, which needs no instrument at all.
- Antenna element geometry is **not** fixed by this decision. Patch dimensions depend
  on the substrate and are a design task, not a consequence of $f_0$.
- Observations O1, O6, O7, O8 and O9 are reclassified rather than closed. O7 continues
  to block calibrated hardware validation.
- EXP-004 stays open until all nine observations are recorded. Its frequency question
  is closed.

## Known limitations

The observed upper limit of 3 GHz is what the instrument displayed, and an instrument
panel sometimes accepts a value beyond the specified range. At 2.44 GHz the design sits
about 19 per cent below that limit, so even a somewhat optimistic reading leaves margin,
but the possibility is recorded rather than dismissed.

Measurement quality at 2.44 GHz is unknown, and analyser performance commonly degrades
towards the top of a band. Nothing in this decision depends on it, and everything about
validating a built board does.

Nothing here has been checked against a datasheet, because no datasheet has been
selected. That remains true until O1 is read.

## Conditions for reopening

- If O1 reveals a model whose specified range stops below 2.44 GHz, so that the panel
  reading was outside specification, reopen immediately. This is the one observation
  that could overturn the decision.
- If O7 establishes that no calibrated reference plane is achievable at 2.44 GHz with
  the hardware present, the frequency stands but hardware validation does not, and the
  conducted only fallback in EXP-004 becomes relevant.
- If the national table of allocations turns out to be more restrictive than the
  European instrument for band 57a, reopen. That check has still not been done.
- If measured accuracy at 2.44 GHz proves too poor to separate the effects under study,
  reopen with the measurement rather than the band as the subject.
