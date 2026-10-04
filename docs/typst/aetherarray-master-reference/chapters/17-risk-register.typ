#import "../template.typ": *

= Part XVII. Risk register <part-xvii-risk-register>

Likelihoods are qualitative, from the evidence named; no numerical probability is supported by
data, and none is given.

=== RF design

#small-table[
#table(
  columns: (3.2fr, 49pt, 3.5fr, 4.0fr, 4.4fr, 3.5fr),
  table.header([Risk], [Likelihood], [Consequence], [Evidence], [Mitigation], [Reopening gate]),
  [state dependent loss exceeds the 0.82 dB imbalance allowance], [moderate to high], [the design check of decision 0007 fails], [0.59 to 0.86 dB for state 7 alone *\[analytical\]*, decision 0009], [coupon attenuation; channel simulation; propagate through the 512 states (section 59.4)], [decision 0009: consider FR408HR (B3) or the hybrid (B4)],
  [phase error from permittivity uncertainty], [high before coupons], [pointing budget exceeded at some angles], [$plus.minus 0.2$ bound gives about 6.3 degrees on state 7 *\[analytical\]*], [measure $epsilon_"eff"$ on coupons; calibrate the model], [coupons outside the bound reopen decision 0009],
  [channel to channel permittivity from the 7628 glass weave], [unknown], [a per channel error coupons cannot remove], [no source quantifies it (I25)], [identical layout; measure per channel state phases (SCH-006)], [channels differing by more than the coupon uncertainty reopen decision 0009],
  [switch isolation at 2.44 GHz low], [moderate], [per channel measurements at the common port corrupted; B2 baseline degraded], [20 dB typical at 2 GHz, nothing at 2.44 GHz (I18)], [read the datasheet curve; prefer conducted labels at element ports], [none; affects one baseline],
  [resonance of the de-selected switched line arm], [unknown], [a sharp state dependent loss and phase excursion in band], [standard switched line hazard *\[to verify\]*], [choose reference arm length; simulate (SIM-003)], [redesign of the 180 degree bit],
  [patch detuning], [moderate to high on the first board], [the antenna misses band 57a], [resonance shift over the permittivity bound exceeds the estimated bandwidth *\[analytical\]*], [coupons on the antenna board; expect a second order], [two misses: RO4350B antenna board (B2)],
  [coupling makes the diagonal model inadequate], [unknown], [G4 fails; counts reopen], [synthetic chart only], [staged promotion: frozen coupling matrix first], [decision 0008 outcomes],
  [switch state repeatability above the floor], [unknown], [the drift experiment measures the switches], [no measurement possible before fabrication (E6)], [measure on the built board before any drift claim], [replace the phase control approach (decision 0003)],
)
]

=== Digital and interface

#small-table[
#table(
  columns: (2.4fr, auto, 2.2fr, 2.4fr, 3.6fr, 1.9fr),
  table.header([Risk], [Likelihood], [Consequence], [Evidence], [Mitigation], [Reopening gate]),
  [logic level incompatibility], [unknown], [switches misread commands], [thresholds unread (H1)], [read datasheet; fallback level translator plus bench threshold measurement], [blocks board release],
  [state correlated noise from the control path], [unknown], [a fake calibration coefficient], [mechanism plausible, magnitude unmeasured], [quiet window, local converter, EXP-005 Phase A], [R9 escalation reopens decision 0005],
  [header cannot supply the board], [unknown], [separate supply, larger ground question], [current limit unread (H2)], [read the limit], [H5 grows],
  [ground loop and EMI over the ribbon], [unknown], [slow offsets, state correlated pickup], [none measured (H5)], [interleaved grounds; C5 strap test], [H5 becomes a measured requirement],
  [gateware effort dominates the schedule], [moderate], [delays every experiment], [no gateware experience recorded in the repository], [phased harness; fallback to a simpler controller for the first campaign], [decision 0005 conditions],
)
]

=== Measurement

#small-table[
#table(
  columns: (2.4fr, auto, 2.2fr, 3.6fr, 3.1fr, 3.2fr),
  table.header([Risk], [Likelihood], [Consequence], [Evidence], [Mitigation], [Reopening gate]),
  [no calibration kit or adapters for the analyser], [moderate], [no calibrated measurement at the SMA plane], [nothing confirmed (O7)], [SCH-001; class 2 interconnect; TRL coupon fallback], [conducted only fallback (decision 0004)],
  [analyser model specified below 2.44 GHz], [low], [the frequency reopens], [the panel read 3 GHz; model unread (O1)], [read the label], [decision 0004 reopens immediately],
  [automation unproven], [moderate], [no unattended analyser runs], [nothing ever enumerated (O9)], [detector path for unattended work], [a dedicated source, class 4],
  [reference plane errors], [moderate], [wrong labels, wrong G4 inputs], [the reference plane is a recurring concern in EXP-011], [coupons C3; explicit planes in every file], [none],
  [room reflections dominate radiated readings], [unknown], [patterns and sensing confounded], [EXP-005 Phase B not run (I3)], [conducted measurement backbone; time gating if K3 installed; absorbers], [acoustic route or conducted only (`docs/uncertainties.md`)],
  [shared analyser access], [moderate], [scheduling delays], [shared with another project (`docs/shared-resources.md`)], [alternate by phase], [none],
)
]

=== Machine learning

#small-table[
#table(
  columns: (2.8fr, 1.5fr, 1.9fr, 1.8fr, 2.6fr, 1.4fr),
  table.header([Risk], [Likelihood], [Consequence], [Evidence], [Mitigation], [Reopening gate]),
  [drift too small to learn], [unknown], [the learning track does not exist], [G2 unanswered], [answer G2 honestly before modelling], [decision 0002 superseded],
  [drift unpredictable, dominated by handling], [unknown], [no prior helps], [I14 open], [log handling; model jumps separately], [decision 0002],
  [dataset too small], [moderate], [weak or seed dependent results], [about 100 sessions a week, unverified], [simple models; long unattended runs], [none],
  [no count advantage over the non learned temporal baseline], [moderate], [the learned contribution is null], [baseline C may capture most of the saving], [report it as the result], [none; a negative result is reported],
  [temporal leakage in evaluation], [low if the protocol is followed], [optimistic results], [standard pitfall], [chronological and rolling origin splits], [none],
  [overconfident prior stops early on a wrong answer], [moderate], [silent calibration error], [section 39.2], [coverage tests; residual check with fallback], [none],
)
]

=== AP-S demonstrator

#small-table[
#table(
  columns: (2.6fr, 1.5fr, 2.1fr, 2.7fr, 2.8fr, 1.8fr),
  table.header([Risk], [Likelihood], [Consequence], [Evidence], [Mitigation], [Reopening gate]),
  [four elements cannot meet a suppression requirement robustly], [unknown], [communication mode weak], [feasibility not studied], [N = 4 feasibility gate with criteria first], [element count reopened by decision],
  [sensing not reproducible at the venue], [moderate to high], [sensing mode fails on site], [venue multipath differs; visitors near the booth], [simplest task; ratio features; recalibration on site], [choose a simpler task],
  [receiver architecture versus the rules], [unknown], [a disallowed or missing source separation], [SDR and receiver rules not found in excerpts], [read the call in full; choose a receiver early], [design change before the proposal],
  [schedule], [high], [no working system by 24 May 2027], [nothing fabricated on 2026-10-04; gates F1 to F5 open], [propose only what can be built; parallelise], [descope to a credible subset],
  [team and mentor not in place], [unknown], [no eligible submission], [not recorded in the repository], [recruit; record], [none],
  [contest facts wrong], [low to moderate], [a non compliant proposal], [snippet level only], [read the official call in full], [correct Part IX],
)
]

=== Project

#small-table[
#table(
  columns: (2.5fr, auto, 1.7fr, 3.3fr, 3.3fr, 1.4fr),
  table.header([Risk], [Likelihood], [Consequence], [Evidence], [Mitigation], [Reopening gate]),
  [HFSS Student does not run on the project computer], [moderate], [the local simulation path is blocked], [SIM-001 failed to open a session twice; low free memory recorded], [interactive first launch; free memory; school full HFSS if needed], [`EITHER` escalation],
  [fabrication delays, second antenna board], [moderate], [schedule slip], [decision 0009 expects a possible second antenna order], [order early once the gate clears], [none],
  [school laboratory availability], [unknown], [bench work delayed], [access terms not recorded (SCH-008)], [runbooks make visits short], [dedicated source purchase],
  [budget, 50 to 70 EUR rule], [moderate], [descoping pressure], [BOM about 62 EUR before connectors], [neutral levers only; never shrink bits or elements silently], [decision 0003],
)
]
