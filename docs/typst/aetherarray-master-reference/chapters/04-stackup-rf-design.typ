#import "../template.typ": *

= Part IV. PCB stack-up and RF physical design <part-iv-pcb-stack-up-and-rf-physical-design>

A *stack-up* is the layer construction of a printed circuit board: which copper and
dielectric layers, in which order, of which thickness and material. For an RF board it decides
the impedance of every line, the phase of every switched length and much of the loss. Decision
0009 selected the Rev A stack-ups on 2026-10-03, recorded as `reva-stackup-r1` in
`hardware/rev-a/stackup/reva-stackup.json`. Every value in that file carries a status, never
mixed: `guaranteed`, a published specification limit; `typical`, a laminate vendor's typical
value and never a tolerance; `nominal`, a value a design tool or a fabricator's calculator uses;
`assumed`, an engineering assumption made in decision 0009; and, for tolerances, `unbounded`,
with no number. The tables below between generation markers come from that file.

== 21\. The beamformer stack-up

=== 21.1 The construction

#include "../generated/stackup-nominal.typ"

The RF microstrip is on L1 over a continuous ground on L2, through one 0.2104 mm layer of 7628
glass prepreg. L3 carries the supply rails and the slow digital lines of decision 0005, and L4
carries digital and connector routing under a ground pour stitched to L2. The keep-out rule keeps
L2 unbroken beneath every RF trace, divider and switch, with at least three prepreg thicknesses
of plane on either side *\[assumed\]*; a line on L3 or L4 that passes beneath RF copper may not
change reference layer there.

=== 21.2 Why this construction

#table(
  columns: (2.9fr, 6.4fr),
  table.header([Advantage], [Explanation]),
  [line width matches the switches], [a 50 ohm seed width of about 0.37 mm against the 0.65 mm pitch of the SC-70-6 package],
  [the widest 50 ohm line of the published single prepreg options], [about four times the 0.09 mm process minimum; finer glass styles give 0.21 mm or less, with 1.8 to 2.8 times the conductor loss],
  [one homogeneous dielectric under the RF], [a single material to model and to calibrate],
  [an inner plane for control routing], [beam state lines cross under RF lines without cutting the RF ground],
  [controlled impedance at no extra charge], [the fabricator commits to this published construction when impedance control is ordered \[#link(<ref-V8>)[V8]\]],
  [cost and lead time], [a low cost class and a few days of production, against one to two project budgets for an RF laminate],
)

#table(
  columns: (1.8fr, 7.4fr),
  table.header([Disadvantage], [Explanation]),
  [loss], [the highest of the compared constructions: dielectric loss alone about 5.3 dB/m],
  [state dependent loss], [the 315 degree state loses 0.59 to 0.86 dB more than the 0 degree state, against an amplitude imbalance allowance of 0.82 dB for everything together (section 59)],
  [coarse glass weave], [7628 cloth has large glass bundles; a 0.37 mm line can see a different local permittivity on different channels],
  [weak permittivity provenance], [a calculator nominal with no frequency and no test method],
)

=== 21.3 Uncertainties, as recorded

#include "../generated/stackup-tolerances.typ"

#table(
  columns: (64pt, 9.8fr, 3.8fr),
  table.header([Uncertainty], [What the sources say], [Consequence]),
  [permittivity provenance and frequency], [4.4 for 7628 prepreg in the fabricator's impedance calculator, no frequency or method stated \[#link(<ref-V8>)[V8]\]; the fabricator says its values are deduced, not the supplier's raw data \[V10\]; the laminate vendor gives 4.2 to 4.4 at 1 GHz for one laminate thickness and 3.9 to 4.1 for another \[#link(<ref-V12>)[V12]\]], [a bound of $plus.minus 0.2$ is adopted *\[assumed\]*; it is an envelope, not a guarantee],
  [core permittivity contradiction], [4.6 on the stack-up page \[#link(<ref-V8>)[V8]\], 4.43 in the calculator guide \[V9\]], [affects no RF line; recorded, not resolved],
  [copper thickness contradiction], [0.035 mm on the stack-up page \[#link(<ref-V8>)[V8]\], 1.6 mil, about 0.041 mm, in the calculator \[V9\]], [bounded as $+ 0$ to $+ 0.0056$ mm; confirmed at order time],
  [impedance tolerance contradiction], [10 per cent on the capabilities page \[V11\], 20 per cent elsewhere \[V10\]], [confirmed at order time],
  [laminate brand], [not guaranteed per order; multilayer boards may use one of several laminates \[#link(<ref-V14>)[V14]\]], [a coupon order does not characterise the production order],
  [glass weave], [no source quantifies the spatial variation], [uncertainty I25; the one material effect a coupon cannot remove],
)

*Why a manufacturer's nominal permittivity is not a measured RF truth.* A permittivity value
is meaningful only with its frequency and its test method. FR-4 permittivity falls slowly with
frequency, and different methods measure different things: Rogers itself publishes a process
value of 3.48 for RO4350B, measured in a clamped stripline at 10 GHz, and a design value of 3.66,
measured by a differential phase length method from 8 to 40 GHz, and its own chart reads higher
still near 2.5 GHz \[#link(<ref-V17>)[V17]\]. A calculator value with neither frequency nor method is a starting
point. The board's own coupons, measured on the analyser, become the authority once a board
exists (section 25).

Order time requirements, from decision 0009: request impedance control with stack-up
JLC04161H-7628 so that the published construction is used; declare the RF nets uncoated and
ask that their widths are not adjusted for a coated model; specify ENIG; record the laminate the
fabricator reports.

== 22\. The antenna stack-up

The antenna board is two layer FR-4, 1.6 mm, with 1 oz finished copper: patches, feed lines and
launches on L1, one unbroken ground on L2. Its core thickness, 1.53 mm, is *\[assumed\]* from
the finished thickness; its permittivity, 4.5, is the fabricator's capability page value with no
frequency *\[vendor nominal\]*; its loss tangent, 0.015, is *\[assumed\]*; and its laminate
brand is one of four \[#link(<ref-V14>)[V14]\]. It is the least well defined material in the project.

The trade-off is the one of section 6.3: a thicker substrate gives a patch more bandwidth and
more radiation efficiency, at the cost of wide feed lines, which on an antenna board with short
feeds and no switches is harmless.

#include "../generated/stackup-patch.typ"

These figures are estimates from the transmission line patch model of Balanis \[#link(<ref-B2>)[B2]\], computed by
`rfkit.stackup.patch_sanity`, and say only that a patch is physically sensible on this
construction. They are not a design: the patch length, width, feed and spacing are free
parameters for HFSS. The resonance shift over the permittivity bound is larger than the
estimated bandwidth, so the first antenna board may not resonate in band 57a; decision 0009
expects that a second antenna board may be ordered, and moves the antenna board to RO4350B
(option B2) if two boards in a row miss the band.

== 23\. Why not a Rogers laminate?

RF laminates such as Rogers RO4350B are designed for this frequency range. Their advantages are
real:

- lower loss: a loss tangent of about 0.0031 at 2.5 GHz against about 0.015 for FR-4 \[#link(<ref-V17>)[V17]\];
- a guaranteed process permittivity tolerance of $plus.minus 0.05$ and guaranteed thickness tolerances
  \[#link(<ref-V17>)[V17]\], where FR-4 offers calculator nominals;
- more uniform glass, so less channel to channel variation.

Decision 0009 compared them, with the same computations applied to every construction:

#include "../generated/stackup-comparison.typ"

And it found three reasons not to choose them for Rev A:

1. *Cost.* At the accessible fabricators, the RF laminate options cost between half and twice
   the whole project budget of 50 to 70 EUR for one board, against a few euros for FR-4.
2. *Fabrication constraints.* At the fabricator that publishes both, RO4350B is two layer only,
   with no stated impedance control; the thin version is a 0.6 mm board with no inner layer for
   control routing, and needs a taper at every switch pin if made thick.
3. *A measurement is needed anyway.* Even Rogers's nominal permittivity is ambiguous at
   2.44 GHz, between a process value, a design value and a chart (section 21.3). Keeping the
   315 degree state within 2.29 degrees needs the beamformer permittivity known to about
   $plus.minus 0.073$ (section 59), which no candidate guarantees as a nominal value. On every
   candidate the effective permittivity must therefore be measured on the board. What differs is
   how much the material varies around the measured value, and how much loss it adds.

*Rogers is a reopening path, not a rejection.* Decision 0009 names the triggers: coupon
measurements outside the assumed bounds, channels differing by more than the coupon uncertainty
(the glass weave effect), a state dependent loss that makes the amplitude imbalance exceed
0.82 dB, two antenna boards missing the band, or a budget change. The first places to look
are FR408HR with spread glass (B3), the Eurocircuits RO4350B and FR-4 hybrid (B4), and RO4350B
for the antenna board (B2).

== 24\. Solder mask and copper roughness

*Solder mask is opened over RF copper.* The fabricator publishes a nominal mask thickness, a
guaranteed minimum of 10 um, no maximum and a permittivity of 3.8 with no frequency \[#link(<ref-V8>)[V8], V11\]. A
mask over the RF lines could therefore be bounded on one side only, and its thickness varies
across a board, which would become channel to channel phase error that no common correction
removes. Opening the mask over RF microstrip and patches removes the parameter: the nominal HFSS
model has no mask on RF copper, matching the fabrication drawing. The price is ENIG on the
exposed lines, whose nickel adds conductor loss; that enters the loss bound and the coupon
attenuation, not the nominal model. The mask stays elsewhere, including the dams between switch
pads.

*Copper is smooth in the nominal model, and its roughness is bounded, not invented.* No
fabricator publishes its foil type or roughness. Rough copper raises conductor loss, because the
current at 2.44 GHz flows within about 1.3 um of the surface and has to follow the roughness,
and it raises the apparent permittivity. A Huray model, which represents the surface as
stacked spheres, needs nodule size and density data that nobody has published for these boards,
so decision 0009 asserts none. Instead, the loss study bounds conductor loss between smooth
copper and twice smooth, the asymptote of the Hammerstad and Jensen roughness correction \[#link(<ref-B8>)[B8]\].
The apparent permittivity rise, which that correction does not capture, is absorbed into the
effective permittivity the coupons measure. The only roughness data found for any candidate was
for Rogers foils, about 3 um for standard 1 oz foil \[#link(<ref-V18>)[V18]\].

== 25\. Coupons

A *coupon* is a small test structure fabricated on the same panel as the real circuit, so that
it shares the circuit's laminate lot, thickness and etch, and can be measured when the circuit
itself cannot be measured in pieces. Decision 0009 defines four, plus an optional calibration
set, on each board; they are defined but not yet laid out.

#table(
  columns: (1.1fr, 3.7fr, 7.1fr),
  table.header([Coupon], [Structure], [What it identifies]),
  [C1], [a 50 ohm thru line between two SMA launches, of the SIM-001 short length], [the impedance of the line as built; with C2, the launches],
  [C2], [the same line made a quarter guided wavelength longer at $f_0$], [with C1, the propagation constant $gamma$ by the two line method: $epsilon_"eff"$ and attenuation of the board as built, which absorb permittivity, thickness, roughness and ENIG together],
  [C3], [two SMA launches back to back with the shortest line], [the launch, so switched line measurements can be de-embedded to the switch reference planes],
  [C4, optional], [a 70.7 ohm line of the C1 length], [the etch on the narrowest line, the Wilkinson arms],
  [TRL set, optional], [thru, reflect and line standards], [only if observation O7 cannot provide a calibration at the SMA plane],
)

*The two line method.* Write the transmission matrix of each measured line as the launch at one
end, the uniform line, and the launch at the other end, $vb(T)_i = vb(X) thin vb(L) ( l_i ) thin vb(Y)$, with $vb(L) ( l ) = op("diag") ( e^(- gamma l) , e^(gamma l) )$.
If the launches are identical, the product

$ vb(M) = vb(T)_"long" thin vb(T)_"short"^(- 1) = vb(X) thin op("diag") lr(( e^(- gamma Delta l) \, e^(gamma Delta l) )) vb(X)^(- 1) $

has eigenvalues $e^(minus.plus gamma Delta l)$ that do not depend on the launches at all. From them:

$ gamma = alpha + j beta , wide epsilon_"eff" = lr(( frac(c thin beta, 2 pi f) ))^2 , wide alpha_"dB/m" = 8.686 thin alpha $

#table(
  columns: (auto, 4.1fr, auto),
  table.header([Symbol], [Meaning], [Unit]),
  [$vb(T)_i$], [measured transmission (cascade) matrix of line $i$, from its S-parameters], [dimensionless],
  [$vb(X)$, $vb(Y)$], [the launch at each end, unknown and cancelled], [dimensionless],
  [$Delta l$], [length difference, a quarter guided wavelength at $f_0$: 17.2 mm on the seed], [m],
)

The quarter wavelength choice matters: at a difference of 0 or 180 degrees the two eigenvalues
coincide and the extraction becomes ill conditioned, which is the same reason line standards in
TRL calibration are chosen near 90 degrees. `rfkit.lineparams` implements this extraction, and
the same code serves SIM-001, whose two simulated line lengths, 10 mm and 27.2 mm, are the coupon
lengths, so simulation and measurement go through the same extraction.

*What coupons do and do not do.* They calibrate the model: a measured $epsilon_"eff"$
or attenuation updates the material values in a new revision of the canonical file and the
models are rerun; that is model calibration and does not reopen decision 0009. They do not replace
knowledge of the stack-up, they are measured only after fabrication, and they cannot detect
channel to channel variation, because they sit in one place on the panel.

*SCH-012*, the stack-up validation at the bench, is NOT READY: the coupons are not laid out, the
extraction procedure and its uncertainty have not been written before data, and the analyser
uncertainty waits on EXP-004 observations O1 and O7 (`docs/runbooks/register.md`).
