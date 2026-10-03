# Rev A stack-up

- Status: selected, `reva-stackup-r1`, decision 0009
- Last reviewed: 2026-10-03

This folder holds the one definition of the Rev A board stack-ups, and the evidence that
chose them.

| File | What it is | Who reads it |
| --- | --- | --- |
| `reva-stackup.json` | **the canonical stack-up**: both boards, every value with unit, status and source | every tool: `rfkit`, the SIM-001 builder, ADS and HFSS set-ups |
| `candidates.json` | the alternatives decision 0009 compared and did not select | nobody but the comparison; never simulated |
| this file | what the fields mean, and how each tool consumes them | people |

Every table between `stackup:begin` and `stackup:end` markers in this file, in decision 0009
and in SIM-001 is generated from the JSON by `python -m rfkit.cli stackup --write-docs`, and
`tools/rfkit/tests/test_stackup.py` fails if one drifts. Edit the JSON, never a table.

## 1. What a stack-up contains here

| Item | Field in `reva-stackup.json` |
| --- | --- |
| fabricator, process, service tier, ordering notes, lead time, cost class | `constructions.<board>.fabrication` |
| laminate family and designation | `materials.<name>.designation` |
| layer count, finished thickness | `layer_count`, `finished_thickness` |
| dielectric between the RF layer and its reference plane | the layers named by `rf_line.substrate_layers` |
| prepreg and core construction | `layers`, in order, as the fabricator publishes them |
| copper on each layer | the thickness of each conductor layer |
| solder mask over RF copper, and whether it is modelled | `soldermask` |
| permittivity and loss tangent, with frequency and method | `materials.<name>.permittivity`, `loss_tangent` |
| copper conductivity and roughness model | `materials.copper`, `simulation_model.copper_roughness` |
| surface finish | `surface_finish` |
| controlled impedance | `fabrication.service_tier` |
| tolerances that move impedance and phase | `tolerances.<board>` |
| trace, space, via and board size rules | `rules` |
| layer allocation and RF keep-out | `layers[].role`, `rf_keepout` |
| source, revision and date of every value | `sources`, referenced by each value's `source` |

Statuses, never mixed: `guaranteed` is a published specification limit or tolerance;
`typical` is a laminate vendor's typical value and never a tolerance; `nominal` is a value a
design tool or a fabricator's calculator uses; `assumed` is an assumption made in decision
0009. A tolerance no source bounds is `unbounded` and has no number.

What the file deliberately does not hold: the working frequency, which is decision 0004's and
is read from `rfkit.budget.F0_HZ`; and any trace width, line length or patch dimension. The
validator rejects those keys, because geometry is decided by SIM-001 and at layout.

## 2. The selected stack-up

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

### Tolerances, for tolerance studies only

Bounds with no distribution. The nominal model never reads them.

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

## 3. Layer allocation

Beamformer: L1 carries the RF microstrip and the RF parts, with digital only as short escapes
outside the RF keep-out; L2 is the continuous RF reference plane, never routed and never
split; L3 carries the supply rails and the slow digital lines of decision 0005; L4 carries
digital and connector routing under a ground pour stitched to L2. The keep-out keeps L2
unbroken beneath every RF trace, divider and switch, with at least three PP1 thicknesses of
plane either side [assumed]; vias through L2 there are ground stitching only, and a line on L3
or L4 crossing beneath RF copper may not change reference layer there.

Antenna board: L1 carries patches, feeds and launches; L2 is one unbroken ground.

## 4. The model decisions that go with it

| Item | Nominal model | Fabrication | Uncertainty kept |
| --- | --- | --- | --- |
| Solder mask on RF copper | absent | opened over RF microstrip and patches | none in the model; the opening is checked on the board |
| Surface finish | not modelled | ENIG | nickel loss, in the loss bound and the coupon attenuation |
| Copper roughness | smooth | foil not published | conductor loss between 1 and 2 times smooth; apparent permittivity rise left to the coupons |
| Dielectric dispersion | values used as given | not applicable | no source at 2.44 GHz; the coupons measure it |
| Reference plane | finite conductivity boundary | 15.2 um inner copper, about eleven skin depths | none significant |

## 5. Derived figures, none of them final

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

<!-- stackup:begin loss -->
| Construction | Conductor loss (dB/m) | Dielectric loss (dB/m) | Extra loss of the 315 degree state, smooth copper (dB) | Same, conductor loss doubled (dB) |
| --- | --- | --- | --- | --- |
| beamformer | 4.49 | 5.29 | 0.59 | 0.86 |
| antenna | 0.59 | 5.60 | 0.36 | 0.39 |
<!-- stackup:end loss -->

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

<!-- stackup:begin patch -->
**SANITY CHECK ONLY.** The patch length, width, feed and spacing stay free parameters for HFSS. These figures only say whether a patch is physically sensible on each construction.

| Construction | $W_p$ (mm) | $L_p$ (mm) | Bandwidth, VSWR 2 | Radiation efficiency | Resonance shift over the permittivity bound |
| --- | --- | --- | --- | --- | --- |
| beamformer | 37.4 | 29.3 | 0.14 per cent | 9 per cent | -2.19 to +2.34 per cent |
| antenna | 37.0 | 28.6 | 1.05 per cent | 48 per cent | -1.06 to +3.38 per cent |

Four elements at half a free space wavelength need an antenna board about 260 mm long, sanity check only.
<!-- stackup:end patch -->

## 6. How each tool reads the same values

**rfkit and scikit-rf.** `rfkit.stackup.load()` reads and validates the file and returns
quantities in SI, with their status and source. `seed`, `sensitivity`, `state_loss_spread_db`
and `patch_sanity` derive the figures above; `sim001_parameters` gives the SIM-001 inputs. A
scikit-rf `MLine` for any later circuit model is built from `Construction.h`, `er`, `tand`,
`t` and `sigma`, never from typed numbers.

**HFSS through PyAEDT.** `tools/sim/sim001_hfss.py` builds SIM-001 from
`sim001_parameters`, and `--dry-run` prints the full geometry without AEDT. Later models
follow the same pattern: import `rfkit.stackup`, read the construction, set the AEDT
materials and variables from it.

**HFSS by hand, or ADS.** `python -m rfkit.cli stackup --json stackup-derived.json` writes
every value and derived seed to a file. In ADS the substrate is entered from the nominal
table: `H` from the RF substrate layer, `Er` and `TanD` from its material, `T` from the
signal copper, `Cond` from copper conductivity, roughness zero, no cover layer. The project or
workspace records the stack-up fingerprint the values came from.

**Measurements.** A Touchstone file from HFSS, ADS or the analyser is loaded with
`load_touchstone(path, source, stackup=st.fingerprint)`. The fingerprint is the identifier
plus the first twelve characters of the file's SHA-256, so an edit that forgot to bump the
revision still shows. Comparison reports print it, and warn when the traces they compare come
from different stack-ups.

**Nominal and tolerance runs are different runs.** A nominal run reads the construction only.
A tolerance run perturbs the inputs named in `tolerances`, one at a time and then at every
corner, and its outputs are labelled as tolerance results. Neither writes back to the file.

## 7. Changing the stack-up

- A measured permittivity or attenuation from the coupons calibrates the model: new revision
  of this file, `id` and `revision` incremented, the measured value with status `nominal` and
  the measurement as its source, docs regenerated. The board does not change, and decision
  0009 is not reopened.
- A different construction, laminate or fabricator is a stack-up replacement: a new decision,
  under the reopening conditions of decision 0009.
- Either way, every result keeps the fingerprint of the stack-up it was produced on.

## 8. Coupons

Defined in decision 0009 and laid out with the boards, not here: a 50 ohm thru line and the
same line a quarter guided wavelength longer, on each board, for the propagation constant by
the two line method; two launches back to back for de-embedding; optionally a 70.7 ohm line,
and a TRL set only if the analyser calibration at the SMA plane cannot be had otherwise. The
two line pair has the same lengths as SIM-001, so simulation and measurement go through the
same extraction.
