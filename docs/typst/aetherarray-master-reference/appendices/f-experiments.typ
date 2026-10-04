#import "../template.typ": *

== Appendix F. Experiment list

#table(
  columns: (auto, 2.8fr, 1.8fr, 1.8fr),
  table.header([ID], [Title], [Status], [Where]),
  [EXP-001], [array simulator with injected defects], [to do], [`LOCAL`],
  [EXP-002], [calibration methods compared in simulation], [to do], [`LOCAL`],
  [EXP-003], [sensitivity to noise and measurement count], [to do], [`LOCAL`],
  [EXP-004], [instrument audit and working frequency], [running; frequency closed; 4 complete, 4 partial, 1 not taken], [`SCHOOL-BENCH`, SCH-001],
  [EXP-005], [repeatability floor and control path], [planned; Phase A ready, not run; Phase B gated], [`LOCAL`, `SCHOOL-BENCH`],
  [EXP-006], [two element array], [to do], [`SCHOOL-BENCH`],
  [EXP-007], [known cable error], [to do], [`SCHOOL-BENCH`],
  [EXP-008], [first real calibration], [to do], [`SCHOOL-BENCH`],
  [EXP-009], [four elements], [to do], [`SCHOOL-BENCH`],
  [EXP-010], [calibration validity over time], [to do; gates the learning track], [`EITHER`],
  [EXP-011], [coupling and gate G4], [planned; criterion fixed; no data], [`EITHER`, `SCHOOL-BENCH`],
  [EXP-012], [measurement count against classical baselines], [to do], [`LOCAL`],
  [EXP-013], [learned first calibration estimator, a control], [to do], [`LOCAL`],
  [EXP-014], [unattended recalibration rig and schema], [to do], [`EITHER`],
  [EXP-015], [learned drift prior against from scratch, the central claim], [to do; needs G2], [`LOCAL`],
)
