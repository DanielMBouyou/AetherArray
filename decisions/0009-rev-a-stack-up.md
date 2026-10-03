# 0009. The Rev A stack-up: four layer FR-4 for the beamformer, two layer FR-4 for the antennas, calibrated by coupons

- Status: accepted
- Date: 2026-10-03
- Scope: the fabrication process, laminate and layer construction of both Rev A boards; the nominal electromagnetic material model; the tolerance bounds; what SIM-001 and every later ADS, HFSS and PyAEDT model read
- Canonical definition: `hardware/rev-a/stackup/reva-stackup.json`, identifier `reva-stackup-r1`

## Question

Which fabrication process and layer construction should each Rev A board use, so that
SIM-001 and every later model can start from traceable material values, without freezing
any RF geometry, and without letting poorly known PCB material dominate the modelling and
calibration errors the project exists to measure?

## Context

Decision 0003 made Rev A two boards: a beamformer and control interface board carrying 29
PE4259-63 switches in SC-70-6 packages, three Wilkinson stages and the detector, and a
passive four element antenna board. It assumed both boards would be two layer FR-4 and that
FR-4 line loss would be tolerable, and left both assumptions to be checked. Decision 0004
fixed $f_0 = 2.44$ GHz and moved every printed length onto the stack-up. Decision 0005 put a
registered buffer and a converter on the beamformer board, so sixteen beam state lines, a
strobe, I2C and two supply rails have to be routed there. Gate F5 of decision 0006 waits on
the stack-up. Decision 0007 recorded two numbers this record has to respect: the hardware's
own state dependent phase error against nominal should stay within 2.29 degrees at $f_0$,
and the amplitude imbalance across channels of one array state within 0.82 dB peak to
peak. The private budget rule is 50 to 70 EUR of new hardware for the whole project, with
about 8 EUR per board in the bill of materials.

Nothing is built. Every figure below is documentation or computation, labelled as such.

### What a stack-up has to contain here

For this repository a stack-up is complete when it states, for each board: the fabricator
and the service tier; the laminate family and designation; the layer count; the finished
thickness; the thickness of the dielectric between the RF layer and its reference plane;
the prepreg and core construction as the fabricator publishes it; the copper on each
relevant layer; whether solder mask covers RF copper and whether it is modelled; the
permittivity and loss tangent, each with the frequency and test method behind it; the
copper conductivity and roughness model; the surface finish; whether controlled impedance
is offered; the tolerances that move impedance and phase; trace, space and via rules; board
size limits; and a source with revision and date for every value that is not trivial.
`hardware/rev-a/stackup/README.md` section 1 maps each item onto a field of the canonical
file.

Every value carries one of four statuses, and they are never mixed: `guaranteed`, a
published fabrication or laminate specification limit; `typical`, a laminate vendor's
typical value, never a tolerance; `nominal`, a value a design tool or a fabricator's
calculator uses; `assumed`, an engineering assumption made here. A tolerance no source
bounds is `unbounded` and carries no number.

### Why material uncertainty matters to this array

A printed line of physical length $L$ has phase

```math
\varphi = \beta L,
\qquad
\beta = \frac{2\pi f \sqrt{\varepsilon_{\text{eff}}}}{c}
```

| Symbol | Meaning | Unit |
| --- | --- | --- |
| $\varphi$ | phase delay of the line | rad |
| $\beta$ | propagation constant, phase part | rad/m |
| $L$ | physical length | m |
| $f$ | frequency, $f_0 = 2.44$ GHz here | Hz |
| $\varepsilon_{\text{eff}}$ | effective permittivity of the microstrip | dimensionless |
| $c$ | speed of light in vacuum | m/s |

The length is fixed when the board is laid out, so an error in $\varepsilon_{\text{eff}}$
scales every electrical length by the same fraction, exactly:

```math
\frac{\delta \varphi}{\varphi} = \sqrt{1 + \frac{\delta \varepsilon_{\text{eff}}}{\varepsilon_{\text{eff}}}} - 1
\approx \frac{1}{2}\,\frac{\delta \varepsilon_{\text{eff}}}{\varepsilon_{\text{eff}}}
```

The quasi-static microstrip model, Pozar equation 3.195, links the effective permittivity to
the substrate permittivity $\varepsilon_r$ through a filling factor $F$:

```math
\varepsilon_{\text{eff}} = \frac{\varepsilon_r + 1}{2} + \frac{\varepsilon_r - 1}{2}\,F,
\qquad
F = \left(1 + \frac{12 h}{W}\right)^{-1/2},
\qquad
\frac{\partial \varepsilon_{\text{eff}}}{\partial \varepsilon_r} = \frac{1 + F}{2}
```

so that, to first order,

```math
\delta \varphi \approx \frac{\theta}{2}\,\frac{1 + F}{2}\,\frac{\delta \varepsilon_r}{\varepsilon_{\text{eff}}}
```

| Symbol | Meaning | Unit |
| --- | --- | --- |
| $h$ | dielectric thickness between the trace and its reference plane | m |
| $W$ | trace width | m |
| $F$ | filling factor, the share of the field the substrate sees beyond the uniform half | dimensionless |
| $\theta$ | designed electrical length, here a bit of 45, 90 or 180 degrees, or all three, 315 | deg |
| $\delta \varepsilon_r$ | error in the substrate permittivity used at layout | dimensionless |

These relations are first order and quasi-static; `rfkit.stackup` evaluates the exact line
model as well, and the test suite holds the two within 10 per cent of each other. Example on
the selected beamformer construction: $W/h \approx 1.77$ gives $F \approx 0.36$ and
$\varepsilon_{\text{eff}} \approx 3.3$ in this closed form, so an error of 0.2 in
$\varepsilon_r$ moves the 315 degree state by about 6.5 degrees, against 2.29.

**Why switched lines are exposed.** The error is proportional, so it is largest on the
longest state: 180 degrees carries four times the error of 45, and the state with all three
bits carries seven times. It is the same for every channel, so it looks harmless, but it
depends on the commanded state. Decision 0007 already showed that such a common proportional
error is not absorbed by the diagonal array state and steers the beam. The tables below give
the size of it for the bounds this record adopts. They are what decides the calibration
strategy; they do not set any line length, which this record does not do.

<!-- stackup:begin pointing -->
Keeping the 315 degree state within 2.29 degrees needs the beamformer substrate permittivity known to plus or minus 0.073, about 1.7 per cent.

| Steering angle (deg) | Pointing budget (deg) | Shift, permittivity bound alone, phase scaled by 2.01 per cent (deg) | Shift, worst corner, phase scaled by 3.67 per cent (deg) |
| --- | --- | --- | --- |
| 0 | 0.585 | 0.000 | 0.000 |
| 15 | 0.605 | 0.654 | 1.191 |
| 30 | 0.675 | 0.668 | 1.221 |
| 45 | 0.827 | 0.194 | 0.354 |

Shift is the worst over the eight command origins, from `rfkit.budget.worst_proportional_pointing_deg`; the budget is decision 0007's pointing bound at that angle.
<!-- stackup:end pointing -->

At 15 degrees the permittivity bound alone already exceeds the pointing budget, and the
worst corner of all four bounds roughly doubles it. A beamformer laid out from a data sheet
permittivity would therefore fail decision 0007's derived requirement before any modelling
error is counted.

No accessible process guarantees the beamformer permittivity to that precision **as a
nominal value**. Rogers guarantees its process value to plus or minus 0.05, which would be
enough, but the same data sheet gives a design value 0.18 higher measured by a different
method, and its own chart reads higher still near 2.5 GHz. So on every candidate the nominal
permittivity has to come from a measurement on the fabricated board. What differs between
candidates is how much the material varies around whatever is measured, and how much loss it
adds.

**Erratum to decision 0007, recorded here and in its known limitations.** Decision 0007
writes "a one per cent common permittivity difference between the tools gives 3.15 degrees
on state 7". The
computation behind it, `worst_proportional_pointing_deg` at a fraction of 0.01, scales the
electrical length by one per cent, which is two per cent of effective permittivity, by the
relation above. The values in decision 0007 are unaffected; only the wording is.

## Options considered

Screened out before the comparison: AISLER, which names no laminate and gives impedance
only as orientation, V24; and PCBWay, which offers RO4003C and RO4350B but published no
price, minimum quantity or impedance statement that could be read, V25.

### Option A: one common stack-up for both boards

Scientifically attractive: one material model, coupons reused, simulation and measurement
compared on one substrate. Three ways to do it were examined.

- **A1, the four layer construction for both.** A patch on L1 over L2 sits on 0.21 mm of
  FR-4: about 0.14 per cent bandwidth and about 9 per cent radiation efficiency, which is not
  a usable antenna. Over L4, with L2 and L3 removed under the array, the patch sees prepreg,
  core and prepreg with two permittivities that the fabricator itself publishes
  inconsistently for the core, 4.6 and 4.43; the beamformer coupons, on L1 over L2, would not
  characterise that core; a four layer board with empty inner layers invites copper balancing
  by the fabricator [assumed], which would put unmodelled metal in the patch substrate; and it
  pays for two layers that do nothing.
- **A2, two layer 1.6 mm FR-4 for both.** A 50 ohm line is about 2.8 mm wide, more than four
  times the 0.65 mm lead pitch of the SC-70-6 switches, so all 87 switch RF pins would need a
  taper; and there is no inner plane, so the beam state lines of decision 0005 would cross
  under the RF lines through cuts in the only ground.
- **A3, RO4350B for both, 0.51 mm and 1.52 mm.** One laminate, but two thicknesses, so not one
  stack-up; the beamformer would be two layer, with the same routing problem as A2; and the
  cost is a multiple of the budget, see below.

### Option B: a construction per board, from one fabricator and one laminate class

- **B1, selected.** JLCPCB four layer FR-4, stack-up JLC04161H-7628, RF on L1 over L2, for the
  beamformer; JLCPCB two layer 1.6 mm FR-4 for the antennas.
- **B2.** As B1, with the antennas on RO4350B 1.52 mm.
- **B3.** OSH Park four layer FR408HR for the beamformer, a named low loss FR-4 class
  laminate with spread glass.
- **B4.** Eurocircuits RF pool, a four layer RO4350B and FR-4 hybrid pooled from one piece. Its
  build-up and price are published only in the online configurator, not as text, so it could
  not be evaluated here. It is the first place to look if B1 is reopened on loss.

### Option C: decide nothing until a coupon panel has been measured

A separate first order of coupons would give a measured $\varepsilon_{\text{eff}}$ before
layout. On FR-4 at this fabricator the laminate brand is not guaranteed from one order to the
next, so a coupon order does not characterise the production order; on RO4350B it would, but
see the cost. SIM-001 needs no fabricated value to start. Coupons belong on the production
panel instead, see the decision.

## Comparison

Computed by `python -m rfkit.cli stackup` from the canonical file and from
`hardware/rev-a/stackup/candidates.json`; nothing in this table is typed by hand. Loss spread
is the extra loss of the 315 degree state over the 0 degree state, with smooth copper and with
conductor loss doubled, the roughness bound below. The patch columns apply the same sanity
check to every construction, which is how the beamformer constructions show they cannot carry
the antennas.

<!-- stackup:begin comparison -->
| Construction | Process | $h$ (mm) | $\varepsilon_r$, status | $\tan\delta$ | $W_{\text{seed}}$ (mm) | $\lambda_g$ (mm) | 315 degree loss spread, smooth to doubled conductor loss (dB) | 315 degree error from the $\varepsilon_r$ bound (deg) | Patch bandwidth, efficiency | Width flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| beamformer, selected | JLCPCB, 4 layer FR-4, 1.6 mm, controlled impedance stack-up JLC04161H-7628 | 0.210 | 4.4, nominal | 0.015 | 0.372 | 68.8 | 0.59 to 0.86 | 6.3, assumed | 0.14 per cent, 9 per cent | none |
| antenna, selected | JLCPCB, 2 layer FR-4, 1.6 mm, 1 oz finished copper | 1.530 | 4.5, nominal | 0.015 | 2.836 | 66.5 | 0.36 to 0.39 | 9.8, assumed | 1.05 per cent, 48 per cent | none |
| ro4350b_thin_2l, candidate | JLCPCB, 2 layer RO4350B, 0.51 mm core, finished 0.6 mm, 1 oz, ENIG | 0.508 | 3.66, typical | 0.0031 | 1.073 | 73.2 | 0.17 to 0.27 | 1.9, guaranteed | 0.39 per cent, 49 per cent | wide: over the SC-70-6 lead pitch, a taper at every switch pin |
| ro4350b_thick_2l, candidate | JLCPCB, 2 layer RO4350B, 1.52 mm core, finished 1.65 mm, 1 oz, ENIG | 1.524 | 3.66, typical | 0.0031 | 3.291 | 72.5 | 0.10 to 0.13 | 1.9, guaranteed | 1.18 per cent, 81 per cent | none |
| fr408hr_4l, candidate | OSH Park, 4 layer FR408HR, 1.6 mm, ENIG | 0.200 | 3.61, typical | 0.009 | 0.405 | 74.7 | 0.46 to 0.73 | 3.0, assumed | 0.15 per cent, 12 per cent | none |
<!-- stackup:end comparison -->

| Criterion | B1 beamformer, JLCPCB 4 layer FR-4 | B1 antennas, JLCPCB 2 layer FR-4 | RO4350B, JLCPCB 2 layer | FR408HR, OSH Park 4 layer | Eurocircuits RF pool hybrid |
| --- | --- | --- | --- | --- | --- |
| Loss at 2.44 GHz | highest of the four; dielectric loss alone about 5.3 dB/m | dielectric dominated, short feeds only | lowest | between | to verify, construction not published |
| Confidence in $\varepsilon_r$ and $\tan\delta$ | calculator nominal with no frequency; laminate brand not guaranteed per order; $\tan\delta$ typical at 1 GHz | nominal with no frequency; brand one of four | guaranteed process tolerance; nominal ambiguous by method | typical at 2 GHz, construction specific table | to verify |
| Prototype availability | 5 pieces, standard | 5 pieces, standard | 5 pieces, RF service | 3 copies | 1 piece, pooled |
| Thickness repeatability | board 10 per cent, prepreg not published | board 10 per cent | guaranteed, 7.5 per cent at 0.51 mm | prepreg 10 per cent, published | to verify |
| Controlled impedance | offered, free, tolerance 10 or 20 per cent by page | not offered on two layer | not stated | not stated | to verify |
| 50 ohm width | 0.37 mm, four times the minimum | 2.8 mm | 1.07 mm | 0.41 mm | to verify |
| Patch at 2.44 GHz | not usable | sensible, see the patch table | best | not usable | not on the same board |
| SMA launch | 1.6 mm board, edge or vertical | 1.6 mm board | 0.6 mm board, edge launch needs a thin board part | 1.6 mm board | 1.0 mm board |
| PE4259 switched lines | width matches the SC-70-6 pads | not applicable | taper at every pin, no inner layer for control | width matches | to verify |
| Compact four element layout | 45 degrees is about 8.6 mm | about 260 mm long board | as B1 | as B1 | to verify |
| Simulation reproducibility | one homogeneous layer under RF | one layer | one layer | one layer | two materials |
| Cost class | low, no quote obtained | low, no quote obtained | from 47 USD, 99.5 USD for 5 within 10 x 10 cm in 2023 | about 120 USD for 3 at 100 x 80 mm | to verify |
| Lead time and supply | 2 to 5 days plus shipping | 1 to 2 days for small boards | 4 to 5 days | 9 to 14 days plus 2 to 4 weeks post; shortage notice 2026-07-21 | 5 working days |

What the RF oriented options actually buy, against the selected FR-4, from the two tables:
the loss spread falls from 0.59 dB to 0.17 dB on RO4350B and to 0.46 dB on FR408HR; the
permittivity error the bounds allow on the 315 degree state falls from 6.3 to 1.9 and 3.0
degrees; RO4350B thickness becomes a guaranteed figure. What they cost: RO4350B at this
fabricator is two layer only, with no stated impedance control and a 0.6 mm board, and both
alternatives cost between half and twice the whole project budget for one board, against a
few euros. Neither removes the need to measure the permittivity on the board, for the reason
given above.

## Evidence

No experimental evidence: nothing is built. The decision rests on fabricator and laminate
documentation consulted on 2026-10-03, entries V8 to V23 in
`docs/references/bibliography.md`, and on computations in `tools/rfkit/stackup.py` with the
pinned environment of `requirements.txt`, scikit-rf 1.12.0. Kinds of evidence:

- fabricator documentation, V8 to V11, V13, V14, V16, V19, V20, V22: stack-ups, capabilities,
  tolerances, lead times;
- laminate vendor documentation, V12, V15, V17, V18, V21: permittivity, loss tangent,
  thickness tolerances, copper roughness;
- simulator vendor documentation, V23: HFSS Student 2025 R2 limits, checked because the
  installed release is 2025 R2;
- computation: scikit-rf `MLine`, Hammerstad and Jensen with Kirschning and Jansen dispersion,
  checked against the zero thickness synthesis in Pozar; the transmission line patch model of
  Balanis; the pointing functions of `rfkit.budget` already used by decision 0007;
- unverified technical opinion, labelled where used: that fabricators add copper balancing to
  empty inner layers, and that three dielectric thicknesses of continuous plane either side of
  an RF trace is enough margin.

No instant quote could be obtained from any fabricator: every quote page needs a browser. Cost
classes are taken from published starting prices and per area prices, never from a quote.

## Decision

**Rev A uses option B1, recorded as `reva-stackup-r1`:** the beamformer and control interface
board on JLCPCB's four layer FR-4 stack-up JLC04161H-7628, with the RF microstrip on L1 over a
continuous L2 ground; the antenna board on JLCPCB's two layer 1.6 mm FR-4. Both are ordered
with ENIG and with solder mask opened over RF copper. The permittivity of each board is
measured on coupons carried by that board, and the electromagnetic models are calibrated to
it. The canonical file holds every value; this record quotes it through generated tables.

<!-- stackup:begin nominal -->
**beamformer**, RF beamformer and control interface board: JLCPCB, 4 layer FR-4, 1.6 mm, controlled impedance stack-up JLC04161H-7628.

| Layer | Material | Role | Thickness | Status | Source |
| --- | --- | --- | --- | --- | --- |
| L1 | copper | RF microstrip, RF components, local escapes outside RF keep-out | 0.035 mm | nominal | V8 |
| PP1 | fr4_prepreg_7628 | RF substrate | 0.2104 mm | nominal | V8 |
| L2 | copper | continuous RF reference plane, no routing, no splits | 0.0152 mm | nominal | V8 |
| CORE | fr4_core_np155f | core | 1.065 mm | nominal | V8 |
| L3 | copper | power rails and slow digital: beam state lines, strobe, I2C, converter | 0.0152 mm | nominal | V8 |
| PP2 | fr4_prepreg_7628 | lower prepreg | 0.2104 mm | nominal | V8 |
| L4 | copper | digital and connector routing, ground pour stitched to L2 | 0.035 mm | nominal | V8 |

**antenna**, four element antenna array board: JLCPCB, 2 layer FR-4, 1.6 mm, 1 oz finished copper.

| Layer | Material | Role | Thickness | Status | Source |
| --- | --- | --- | --- | --- | --- |
| L1 | copper | patches, feed lines, SMA launches | 0.035 mm | nominal | V11 |
| CORE | fr4_two_layer | RF substrate | 1.53 mm | assumed | D0009 |
| L2 | copper | continuous ground under every patch and feed, no routing | 0.035 mm | nominal | V11 |

| Material | Designation |
| --- | --- |
| copper | electrodeposited copper, foil type not published by the fabricator |
| fr4_prepreg_7628 | 7628 glass prepreg, resin content 49 per cent, in the fabricator's NP-155F based stack-up; brand not guaranteed per order |
| fr4_core_np155f | NP-155F core assumed by the fabricator's calculator |
| fr4_two_layer | two layer FR-4 core; brand not fixed by the fabricator, one of NP-140F, KB-6164, S1141 or S1000H (V14) |
| lpi_soldermask | liquid photoimageable solder mask |

| Material | Property | Value | Status | Source | Frequency and method |
| --- | --- | --- | --- | --- | --- |
| copper | conductivity | 5.8e+07 S/m | assumed | D0009 | not applicable |
| fr4_prepreg_7628 | permittivity | 4.4 | nominal | V8 | not stated; fabricator impedance calculator value, no frequency stated |
| fr4_prepreg_7628 | loss tangent | 0.015 | typical | V12 | 1 GHz; IPC-TM-650 2.5.5.9 |
| fr4_core_np155f | permittivity | 4.6 | nominal | V8 | not stated; fabricator impedance calculator value, no frequency stated |
| fr4_core_np155f | loss tangent | 0.015 | typical | V12 | 1 GHz; IPC-TM-650 2.5.5.9 |
| fr4_two_layer | permittivity | 4.5 | nominal | V11 | not stated; fabricator capability page value for two layer boards, no frequency stated |
| fr4_two_layer | loss tangent | 0.015 | assumed | D0009 | not stated |
| lpi_soldermask | permittivity | 3.8 | nominal | V8 | not stated; fabricator impedance calculator value |
<!-- stackup:end nominal -->

### Why this, and not a common stack-up or an RF laminate

- **Two constructions, because the physics of the two boards differs by an order of
  magnitude.** The switched line board needs a thin dielectric, for a line as wide as the
  switch pads and an inner plane for the control routing; the patches need a thick one. The
  patch table shows a factor of about seven in bandwidth and five in efficiency. One fabricator
  and one laminate class keep the process and the documentation common.
- **FR-4, because its uncertainty can be measured away and its cost fits.** No candidate makes
  the nominal permittivity known well enough without a measurement on the board; FR-4's larger
  lot to lot spread is then removed by coupons on the same board, and what remains is the
  spatial variation, discussed below. The RF laminates would cost one to two project budgets
  for the beamformer alone.
- **JLC04161H-7628 among the published four layer stack-ups,** because it gives the widest 50
  ohm line of the four single prepreg options: about four times the 0.09 mm process minimum,
  the lowest conductor loss of the four, and one homogeneous prepreg under the RF trace. The
  finer glass styles, 2116, 3313 and 1080, give 50 ohm lines of 0.21 mm or less, at most 2.3
  times the minimum, with 1.8 to 2.8 times the conductor loss, computed with the same line
  model and loss tangent. The cost of choosing 7628 is its coarse glass weave, below.

### Layer allocation, conceptual

| Layer | Beamformer board | Antenna board |
| --- | --- | --- |
| L1 | RF microstrip, switches, divider, detector input, SMA launches; digital only as short escapes outside the RF keep-out | patches, feed lines, SMA launches |
| L2 | continuous ground, the RF reference plane: no routing, no splits | continuous ground |
| L3 | 3.3 V and 5 V rails; beam state lines, strobe, I2C, converter | not present |
| L4 | digital and connector routing, ground pour stitched to L2 | not present |

The keep-out: L2 stays unbroken beneath every RF trace, divider and switch, with at least
three PP1 thicknesses of plane either side [assumed]; vias through L2 there are ground
stitching only; a signal on L3 or L4 that passes beneath an RF trace is shielded by L2 and
does not change reference layer there. No component is placed and nothing is routed by this
record.

### Solder mask: opened over RF copper, and absent from the model

The fabricator publishes a nominal mask of 0.6 mil over traces and 1.2 mil over bare
substrate with a permittivity of 3.8, and a guaranteed minimum of 10 um, but no maximum and no
frequency. A mask over the RF lines could therefore be bounded from one side only, and its
thickness varies across the board, which would turn into channel to channel phase. Opening it
over RF microstrip and patches removes that parameter: the HFSS nominal model has no mask on
RF copper, matching the fabrication drawing. The mask stays elsewhere, including the dams
between the switch pads. The price is ENIG on exposed lines, whose nickel adds conductor loss;
that enters the loss bound and the coupon attenuation, not the model. The fabricator's
impedance calculator assumes coated lines, so the order must declare the RF nets uncoated and
ask that their widths are not adjusted for a coated model.

### Copper roughness: smooth in the nominal model, bounded in the loss study

No fabricator publishes its foil or its roughness. The nominal model uses smooth copper. The
loss study bounds conductor loss between smooth and twice smooth, the asymptote of the
Hammerstad and Jensen correction; no roughness parameter is asserted, and no Huray parameter
is invented. Rough foil also raises the apparent permittivity, which the Hammerstad and Jensen
form does not capture; the coupon extraction absorbs it into the measured
$\varepsilon_{\text{eff}}$.

### Tolerances, kept apart from the nominal model

All four reserved inputs exist for both boards: dielectric thickness, permittivity, copper
thickness and etched width. They are bounds, with no distribution, because no source gives
statistics. The nominal simulation uses the construction values; a tolerance simulation
perturbs one input at a time and then every corner, and never feeds back into the nominal
file.

<!-- stackup:begin tolerances -->
| Construction | Tolerance | Input | Bound | Status | Source |
| --- | --- | --- | --- | --- | --- |
| beamformer | rf dielectric thickness | $h$ | minus 10 to plus 10 per cent | assumed | V11 |
| beamformer | rf dielectric permittivity | $er$ | minus 0.2 to plus 0.2 | assumed | D0009 |
| beamformer | rf copper thickness | $t$ | minus 0 to plus 0.0056 mm | assumed | V9 |
| beamformer | etched width | $w$ | minus 20 to plus 20 per cent | guaranteed | V11 |
| antenna | rf dielectric thickness | $h$ | minus 10 to plus 10 per cent | assumed | V11 |
| antenna | rf dielectric permittivity | $er$ | minus 0.3 to plus 0.1 | assumed | D0009 |
| antenna | rf copper thickness | $t$ | unbounded, no number | unbounded | V11 |
| antenna | etched width | $w$ | minus 20 to plus 20 per cent | guaranteed | V11 |
<!-- stackup:end tolerances -->

<!-- stackup:begin sensitivity -->
Each bound applied alone at the seed width, then the worst of every corner. Phase is the error of a line laid out for the nominal permittivity.

| Construction | Tolerance | Status | $Z_0$ (ohm) | 180 degree error (deg) | 315 degree error (deg) |
| --- | --- | --- | --- | --- | --- |
| beamformer | rf dielectric thickness | assumed | 46.9 to 52.8 | +0.76 to -0.67 | +1.34 to -1.16 |
| beamformer | rf dielectric permittivity | assumed | 51.0 to 49.0 | -3.62 to +3.55 | -6.34 to +6.21 |
| beamformer | rf copper thickness | assumed | 50.0 to 49.7 | +0.00 to -0.37 | +0.00 to -0.65 |
| beamformer | etched width | guaranteed | 56.3 to 45.0 | -2.10 to +1.78 | -3.68 to +3.12 |
| beamformer | worst corner of the bounds above | combined | 41.1 to 60.5 | 6.60 | 11.56 |
| antenna | rf dielectric thickness | assumed | 46.9 to 52.9 | +0.70 to -0.60 | +1.22 to -1.05 |
| antenna | rf dielectric permittivity | assumed | 51.6 to 49.5 | -5.57 to +1.82 | -9.75 to +3.19 |
| antenna | etched width | guaranteed | 56.7 to 44.8 | -1.90 to +1.63 | -3.33 to +2.86 |
| antenna | rf copper thickness | unbounded | not computed | not computed | not computed |
| antenna | worst corner of the bounds above | combined | 41.4 to 61.6 | 7.88 | 13.80 |
<!-- stackup:end sensitivity -->

### Loss

<!-- stackup:begin loss -->
| Construction | Conductor loss (dB/m) | Dielectric loss (dB/m) | Extra loss of the 315 degree state, smooth copper (dB) | Same, conductor loss doubled (dB) |
| --- | --- | --- | --- | --- |
| beamformer | 4.49 | 5.29 | 0.59 | 0.86 |
| antenna | 0.59 | 5.60 | 0.36 | 0.39 |
<!-- stackup:end loss -->

The beamformer's state dependent loss is 0.59 dB with smooth copper and 0.86 dB with conductor
loss doubled, against an amplitude imbalance allowance of 0.82 dB for everything together.
This is the one place where the selected material presses on an accepted decision. It is
deterministic and calculable, not an uncertainty, so it does not corrupt the comparison of
models with measurements, but it can fail the design check of decision 0007. It is recorded as
a known limitation with a reopening trigger, not hidden.

### Antennas: a patch is sensible on the antenna construction

<!-- stackup:begin patch -->
**SANITY CHECK ONLY.** The patch length, width, feed and spacing stay free parameters for HFSS. These figures only say whether a patch is physically sensible on each construction.

| Construction | $W_p$ (mm) | $L_p$ (mm) | Bandwidth, VSWR 2 | Radiation efficiency | Resonance shift over the permittivity bound |
| --- | --- | --- | --- | --- | --- |
| beamformer | 37.4 | 29.3 | 0.14 per cent | 9 per cent | -2.19 to +2.34 per cent |
| antenna | 37.0 | 28.6 | 1.05 per cent | 48 per cent | -1.06 to +3.38 per cent |

Four elements at half a free space wavelength need an antenna board about 260 mm long, sanity check only.
<!-- stackup:end patch -->

A microstrip fed patch on the 1.53 mm core is physically sensible at 2.44 GHz: a few
centimetres on a side, about one per cent bandwidth and an efficiency near one half from the
FR-4 loss. Its resonance is not assured on the first board: the permittivity bound moves it by
more than its own bandwidth. All patch dimensions, the feed and the spacing stay free
parameters for HFSS.

### Coupons, defined and not laid out

Each board carries its own coupons, on the board itself so that they share its laminate lot:

| Coupon | What it removes |
| --- | --- |
| C1, a 50 ohm thru line between two SMA launches, the SIM-001 short length | the impedance of the line as built, and with C2 the launch |
| C2, the same line made a quarter guided wavelength longer at $f_0$ | with C1, the propagation constant by the two line method: $\varepsilon_{\text{eff}}$ and attenuation of the board as built, which absorbs permittivity, thickness, roughness and ENIG together |
| C3, two SMA launches back to back with the shortest line | the launch, so switched line measurements can be de-embedded to the switch reference planes |
| C4, optional, a 70.7 ohm line of the C1 length | the etch on the narrowest line, the Wilkinson arms |
| TRL set, optional | only if EXP-004 observation O7 cannot provide a calibration at the SMA plane; not required by the present measurement architecture |

The antenna board carries C1 and C2 at its own 50 ohm width; with them the patch model is
calibrated to the antenna substrate rather than to the beamformer's.

### SIM-001 is ready

The gate and its evidence are in `experiments/SIM-001-microstrip-50-ohm.md`. The analytical
width is a seed, $W_{\text{seed}} \neq W_{50}$: SIM-001 decides the width, and nothing here
enters KiCad as a rule.

<!-- stackup:begin seeds -->
**INITIALISATION ONLY.** $W_{\text{seed}} \neq W_{50}$. SIM-001 decides the width; every length below is a feasibility estimate, not a layout value.

| Construction | Quantity | Value |
| --- | --- | --- |
| beamformer | $W_{\text{seed}}$ for 50 ohm | 0.372 mm |
| beamformer | closed form check, zero thickness | 0.402 mm |
| beamformer | $\varepsilon_{\text{eff}}$ at $f_0$ | 3.191 |
| beamformer | $\lambda_0$ | 122.9 mm |
| beamformer | $\lambda_g$ | 68.8 mm |
| beamformer | line for 45 degrees | 8.6 mm |
| beamformer | line for 90 degrees | 17.2 mm |
| beamformer | line for 180 degrees | 34.4 mm |
| beamformer | line for 315 degrees | 60.2 mm |
| beamformer | $W_{\text{seed}}$ for 70.7 ohm, Wilkinson arms | 0.182 mm |
| beamformer | width flags | none |
| antenna | $W_{\text{seed}}$ for 50 ohm | 2.836 mm |
| antenna | closed form check, zero thickness | 2.876 mm |
| antenna | $\varepsilon_{\text{eff}}$ at $f_0$ | 3.415 |
| antenna | $\lambda_0$ | 122.9 mm |
| antenna | $\lambda_g$ | 66.5 mm |
| antenna | line for 45 degrees | 8.3 mm |
| antenna | line for 90 degrees | 16.6 mm |
| antenna | line for 180 degrees | 33.2 mm |
| antenna | line for 315 degrees | 58.2 mm |
| antenna | width flags | none |
<!-- stackup:end seeds -->

## Consequences

For simulation:

- SIM-001 can run now, locally on HFSS Student, from `tools/sim/sim001_hfss.py`, which reads the
  canonical file.
- Every model, HFSS, ADS, scikit-rf or PyAEDT, reads `reva-stackup.json`, directly or through
  `python -m rfkit.cli stackup --json`. Numbers are never retyped; the tables in the
  documentation are generated and the tests fail if they drift.
- Every Touchstone file from a model or an analyser carries the stack-up fingerprint in its
  provenance, so a VNA result is traceable to the stack-up its model used, and a comparison
  across stack-ups is flagged.
- A measured $\varepsilon_{\text{eff}}$ from the coupons **calibrates the model**: it updates
  the material values in a new revision of the canonical file, with status `nominal` and the
  measurement as source, and reruns the models. It does not change the board. That is not a
  stack-up replacement and does not reopen this decision.
- Line lengths, the patch and the Wilkinson are still not dimensioned. They follow SIM-001 and
  later simulations, at layout.

For fabrication:

- Gate F5 of decision 0006 is half cleared: the stack-up is chosen; the line lengths are not
  derived yet.
- The order must request impedance control with stack-up JLC04161H-7628 so that the published
  construction is used, declare RF nets uncoated, specify ENIG, and record the laminate the
  fabricator reports. The impedance tolerance stated by the fabricator differs between pages,
  10 and 20 per cent, and is confirmed at order time.
- The beamformer board fits the 102 x 102 mm price class only if the layout allows; the antenna
  board, about 260 mm long, does not, and stays below the 650 square centimetre surcharge.
- A second antenna board order should be expected if the first resonance misses the band.
- Work created: the coupons at layout; the SIM-001 run; a stack-up validation measurement at
  the bench, SCH-012 in the register, once boards exist.

For the repository:

- `CONVENTIONS.md` gains the `SIM-NNN` identifier, for a solver run that fixes a design input
  rather than testing a hypothesis about the array; SIM-001 is the first. Recorded here, as
  that file asks of any change to it.
- `tools/sim/` holds solver model builders that read the canonical stack-up.

## Known limitations

- **State dependent loss.** 0.59 to 0.86 dB on the beamformer against the 0.82 dB allowance of
  decision 0007, before any other contribution. FR-4 dielectric loss alone is about 0.32 dB of
  it and does not depend on the line width.
- **The permittivity is known a priori only to an assumed bound,** plus or minus 0.2 on the
  beamformer, which is about three times what the 2.29 degree requirement would need. The
  bound is an envelope of published values, not a guarantee, and the laminate brand is not
  guaranteed per order. The coupon is the authority once a board exists.
- **Spatial variation is not quantified.** 7628 is a coarse glass weave; a 0.37 mm line runs
  over glass bundles and resin gaps of comparable size, so different channels can see different
  local permittivity. No source quantifies it. It is the one material effect a coupon cannot
  calibrate away, because it differs between channels. Mitigations belong to layout and are not
  decided here.
- **The antenna laminate is undefined:** construction not published, brand one of four, loss
  tangent assumed. Its patch resonance on the first board is uncertain by more than its
  bandwidth.
- **Conflicting fabricator figures** are recorded, not resolved: core permittivity 4.6 or 4.43,
  impedance tolerance 10 or 20 per cent, outer copper 0.035 mm or 1.6 mil. The first affects no
  RF line; the other two are bounded or confirmed at order time.
- **No quote** was obtained from any fabricator.
- **Unverified opinions** used: copper balancing on empty inner layers, and the three thickness
  keep-out margin.

## Conditions for reopening

Model calibration, which does **not** reopen this decision:

- The coupons give an $\varepsilon_{\text{eff}}$ or an attenuation different from the nominal
  model, inside the bounds: update the material values in a new canonical revision and rerun.

Stack-up replacement, which **does** reopen it:

- The selected material or stack-up JLC04161H-7628 becomes unavailable, or the fabricator
  changes its construction or the L1 to L2 dielectric thickness.
- Controlled impedance, the uncoated RF nets or the ENIG finish cannot be ordered as documented.
- Coupon extraction shows the effective permittivity outside the assumed bounds, or channels on
  one board differing by more than the coupon uncertainty, which would be the glass weave
  effect: consider FR408HR with spread glass, option B3, or the Eurocircuits hybrid, B4.
- The state dependent loss, from the coupon attenuation or from a simulation of the switched
  line channel, makes the amplitude imbalance of one array state exceed 0.82 dB: consider B4 or
  B3.
- An antenna simulation shows the two layer construction cannot give a matched patch at
  $f_0$, or two antenna boards in a row miss the band: move the antenna board to RO4350B,
  option B2.
- Cost or lead time makes the process inaccessible, or the budget rule changes enough to make
  an RF laminate affordable.
- Decision 0003 changes the board split, the switch package or the bit set, or decision 0007's
  limits change.
