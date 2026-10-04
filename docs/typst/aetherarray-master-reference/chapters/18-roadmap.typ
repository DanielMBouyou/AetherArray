#import "../template.typ": *

= Part XVIII. Roadmap <part-xviii-roadmap>

From 2026-10-04, ordered by the repository's dependencies; dates are given only where an external
deadline exists. Where a task runs follows the repository's classes.

#small-table[
#table(
  columns: (auto, 2.7fr, 2.0fr, 3.5fr, 2.1fr, 1.8fr),
  table.header([Phase], [Objective], [Prerequisites], [Output], [Gate], [Where]),
  [0a], [finish the analyser audit], [none], [O1, O6 to O9 recorded], [unblocks class 2 purchases; F1], [`SCHOOL-BENCH`, SCH-001 READY],
  [0b], [unblock HFSS Student], [AEDT Student opened once by hand; memory freed], [a working scripted session], [none], [`LOCAL`],
  [0c], [EXP-005 Phase A, condition C1 first], [B1 to B5 confirmed; harness], [V1 to V4, the floor; then C2 to C5], [R9, H3; detector purchase; F2], [`LOCAL`],
  [0d], [read the PE4259 datasheet by hand], [the file], [isolation at 2.44 GHz, input thresholds, truth table], [H1 inputs; I18], [`LOCAL`],
  [0e], [decide the AP-S direction], [the official call read in full; a team and a mentor], [a decision record; a proposal plan], [the 31 December 2026 deadline], [`LOCAL`],
  [0f], [build the array simulator, EXP-001, then EXP-002 and EXP-012], [none], [the virtual bench; measured counts for the baselines, including the fast amplitude only method], [needed before any learning claim], [`LOCAL`],
  [1], [SIM-001, a genuine HFSS run], [0b], [$W_50$, $epsilon_"eff"$, attenuation, with provenance], [the SIM-001 criterion], [`LOCAL`],
  [2], [phase line and Wilkinson simulations, SIM-002], [1], [arm geometries], [criteria registered first], [`LOCAL`],
  [3], [switched line bit and eight states, SIM-003 and SIM-004], [2; a switch model], [state dependent phase and loss], [decision 0007 comparison], [`EITHER`],
  [4], [divider, SIM-005], [1], [balance, isolation, match], [criterion registered first], [`LOCAL`],
  [5], [antenna, SIM-006], [antenna construction], [patch geometry], [criterion registered first], [`LOCAL`],
  [6], [coupling and array, EXP-011 Stage 1 and SIM-008], [5], [$vb(S)_A$, patterns, G4 verdict; system model], [decision 0008], [`EITHER`],
  [7], [schematic re-capture with H1 to H5 closed or decided], [0c, 0d; part choices], [a schematic matching decision 0005], [F4], [`LOCAL`],
  [8], [EXP-005 Phase B with class 2 purchases], [0a, 0c; Phase B rules written], [the RF repeatability floor on both routes], [F3], [`SCHOOL-BENCH`, SCH-003],
  [9], [layout and fabrication], [1 to 7 for lengths and widths; F1 to F5], [Rev A boards with coupons], [F1 to F5], [`LOCAL`, then the fabricator],
  [10], [coupon and VNA characterisation], [9; the O7 calibration chain], [measured $epsilon_"eff"$, attenuation, launches; stack-up revision], [SCH-012], [`SCHOOL-BENCH`],
  [11], [full Rev A characterisation], [10], [per state phases and losses, divider, reflections, labels, detector; E6], [SCH-006; EXP-011 Stage 2], [`SCHOOL-BENCH`],
  [12], [radiated experiments], [11; Phase B floor], [EXP-006 to EXP-009, including the known cable error EXP-007], [lifts decision 0007's provisional status if EXP-007 agrees], [`SCHOOL-BENCH`, SCH-007],
  [13], [drift dataset], [11; gateware; unattended rig], [EXP-010 and EXP-014 data], [*G2*], [`EITHER`],
  [14], [simple temporal baselines], [13], [baselines A to D], [none], [`LOCAL`],
  [15], [learned prior, EXP-015], [13, 14], [$M_"required"$ curves against baselines], [failure declared by the pre-registered rule], [`LOCAL`],
  [16], [active measurement selection], [15], [information gain schedule against fixed schedules], [none], [`LOCAL`],
  [17], [AP-S COMM and SENSE demonstrator], [11 at least; a receiver; gateware; a dashboard], [the contest system], [the contest's final materials, 24 May 2027], [`EITHER`],
)
]

*A plain reading of the calendar.* The contest's preliminary design is due on 31 December 2026,
about three months from now. A credible proposal can be written from the design, the decisions,
the simulations done by then and a clear plan; it cannot honestly report a learned recalibration
result. The final materials are due on 24 May 2027 and must include measurement results. Reaching a
working demonstrator by then requires fabrication early in 2027, which in turn requires phases 0
to 9 to clear in the coming months. If that is not achievable, a demonstrator whose calibration is
classical, with the learned prior presented as ongoing research, would still be truthful.
