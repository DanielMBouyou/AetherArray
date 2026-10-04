#import "../template.typ": *

== Appendix D. Open hardware items, gates and requirements

*Open items, `docs/architecture/control-architecture.md` section 8.* H1 logic level
compatibility, blocks board release; H2 expansion header supply capability; H3 converter part,
decided by EXP-005; H4 buffer part; H5 ground strategy between the boards. All open.

*Pre-fabrication gate, decision 0006.* F1 EXP-004 closed, O1 checked against the model's
datasheet, O7 calibration chain settled: open. F2 EXP-005 Phase A complete with R9 and H3 applied:
open. F3 EXP-005 Phase B complete on both routes, by rules written before data: open, rules not
written. F4 schematic re-captured, H1 to H4 closed, H5 decided: open. F5 stack-up chosen and line
lengths derived: half met, the stack-up is chosen.

*Research gates.* G1 phase measurable: closed, passed (decision 0004). G2 drift above the
repeatability floor: open; floor before fabrication (F3), drift after it (EXP-010). G3 element and
bit count: closed, four and three (decision 0003). G4 coupling model adequacy: criterion fixed
(decision 0008), no data. G5 budget: at order time.

*Requirements, `docs/hardware/rev-a-requirements.md`.* R1 per element connectors; R2 drive one
element, receive on another; R3 scalar power sense at the sum port, digitised on the board; R4
temperature sensors near the phase network and the detector; R5 commanded word recorded; R6 at
least four elements; R7 a documented reference channel; R8 timestamped logging with the fixed
schema; R9 deterministic application and quiet window, adopted as a precaution and tested by
EXP-005. R1, R2, R4, R6, R7 and R9 are not retrofittable.
