# What is established, assumed, or still to verify

- Status: in progress
- Last reviewed: 2026-09-21

---

## 1. Established

| Fact | Source | Consequence |
| --- | --- | --- |
| One centimetre of coaxial cable is about 44 degrees of phase at 2.4 GHz | calculation from the velocity factor | calibration is mandatory, not optional |
| Phase errors with 30 degree standard deviation cost about 1.2 dB of gain | classical array result | the effect is calculable before any measurement |
| Spacing beyond half a wavelength creates grating lobes | the non aliasing condition | a hard geometric constraint |
| Far field distance is about twice the array size squared over the wavelength | usual definition | sets the measurement distance |
| A human body near the setup changes the measurement | absorption and reflection | the measurement protocol has to account for it |
| The required phase depends on frequency | form of the array factor | pointing drifts across the band |
| A full wave electromagnetic simulator is available | tool inventory | the coupling model can come from physics rather than invention |

## 2. Assumed

| Assumption | Why | How it could fall | Effect |
| --- | --- | --- | --- |
| Pattern measurements are possible in an ordinary room | with care, many people manage it | if reflections dominate | move to conducted measurement, or to an acoustic array |
| Coupling is secondary to channel errors | half wavelength spacing | if coupling is strong | the full matrix has to be estimated, so more measurements |
| A classical calibration method will be enough | maturity of the field | if it fails against noise or coupling | optimisation becomes necessary, which is interesting |
| Two elements are enough to validate the method | the physics is the same | if the interesting phenomena start at four | move to four sooner |
| An acoustic array is a good substitute for the algorithms | identical mathematical formalism | if the physical differences change the conclusions | validate on both, which is the interesting experiment anyway |
| Simulated coupling matches measured coupling | full wave simulation is generally accurate | if the model omits the real environment | the gap becomes a result in itself |

## 3. To verify

| N | Question | Method | Blocks |
| --- | --- | --- | --- |
| I1 | Can received power be measured repeatably? | EXP-005 | all of the hardware track |
| I2 | Does the network analyser offer time domain gating to isolate the direct path? | EXP-004 observation O8 | measurement quality. **Not a gate**: the function is optional on some instrument families and built in on others, so its absence is a cost, not a blocker |
| I3 | How large are the reflections in the available environment? | EXP-005 | choice of measurement strategy |
| I4 | Can we measure phase, or only power? | EXP-004 observations O4 and O5 | choice of calibration method, and **gate G1**. If it fails, B5 is unavailable and the per element complex label that supervises the learned drift prior has to be found another way or abandoned, which reopens decision 0002 |
| I5 | How large are channel errors in a home built assembly? | EXP-006 | calibration sizing |
| I6 | Is coupling significant at the chosen spacing? | S parameters between elements, and simulation | complexity of the model |
| I7 | What do commandable phase shifters cost? | component search | architecture choice |
| I8 | How long does a calibration stay valid? | EXP-010 | practical use of the system |
| I9 | Is an angular positioner necessary, and can we build one? | trial | feasibility of pattern measurement |
| I10 | Is the FPGA genuinely useful here? | architecture choice | this project's role in the lab |
| I11 | Does simulated coupling match measured coupling? | simulation then measurement | credibility of the simulation study |
| I12 | Is drift over hours larger than the repeatable measurement floor? | EXP-005 then EXP-010 | **the entire learning track, gate G2** |
| I13 | How much does the power detector itself drift with temperature? | **partly answered**: the AD8318 data sheet, revision E, gives a stability over temperature of $\pm 0.5$ dB across its full range, bibliography V6. Bench measurement over a laboratory swing still to do | whether a null result on I12 is physical or instrumental. Now bounded and correctable, but only if the temperature beside the detector is logged |
| I14 | Is drift driven by time and temperature, or by connector handling? | EXP-014, with handling logged per session | whether a learned prior is possible in principle |
| I15 | How many unattended calibration sessions per day can the rig sustain? | EXP-014 | the data budget, and therefore the model class |
| I16 | Does the generic $4N-4$ phase retrieval bound apply to the structured rotating element measurement set? | reading A12 in full, then a numerical check | whether section 3 of the calibration architecture holds as stated |
| I17 | Can the analyser reach 2.44 GHz? | EXP-004 observation O2 | **answered yes on 2026-09-20**: a ZVL covering 9 kHz to 3 GHz, with transmission and complex formats. The frequency is not frozen only because O1, the exact model, has not been read and every reading is checked against the datasheet of the exact model |
| I18 | What is the PE4259-63 isolation at the working frequency, and is there a guaranteed minimum? | read the curve in the vendor datasheet, which is a scanned image and needs a human | the floor of the B2 baseline taken at the sum port. Only typical spot values are in hand, 30 dB at 1000 MHz and 20 dB at 2000 MHz; no guaranteed figure at any frequency |
| I19 | Is a calibration kit present, and are there adapters from N to the board's SMA plane? | EXP-004 observation O7 | **now the most consequential practical gap.** Without them there is no calibrated measurement at the board reference plane at any frequency. The kits named in the laboratory inventory are 3.5 mm and belong to a different instrument |
| I20 | Which options are installed on the analyser, and what does each designation mean? | EXP-004 observation O8 records the list verbatim; the meaning is then read from the manual for the model O1 returns | decides the echo strategy for EXP-005 and whether a spectrum cross check exists without a second instrument. **The option designations circulating in distributor listings are not confirmed against manufacturer documentation and are not relied on** |
| I21 | Are the instruments in the laboratory inventory physically present? | look for them | every cross check in `docs/hardware/measurement-bench.md` is conditional on this. The measurement plan is built so that the observed analyser alone is sufficient |

Question I10 deserves to be asked bluntly. If the chosen architecture is analogue,
the FPGA has no role in this project, and that should be stated rather than dressed
up with an artificial one. `docs/hardware/rev-a-requirements.md` section 6 now answers
it that way for Rev A: no method in the selected calibration architecture needs one.

I12 is the most consequential open question in the repository. Decision 0002 commits
the project to a learning track that does not exist if the answer is no, and the
answer costs nothing but bench time with instruments already owned.

## 4. Reasoning traps to avoid

- **Measuring a pattern without characterising the environment.** Echoes can produce
  curves that look like lobes.
- **Attributing to coupling what comes from the cables.** The two are confounded in
  the measurement, and separating them needs a protocol.
- **Comparing calibration methods without counting the measurements.**
- **Concluding from a single defect draw.** Results vary a lot from draw to draw.
- **Forgetting that the operator is part of the setup.**
- **Believing a calibration is permanent.** That is exactly what has to be measured.
- **Using the FPGA because it is available**, when the chosen architecture has no
  need for one.
- **Trusting simulated coupling without checking it against measurement.**
