// GENERATED FILE, do not edit by hand.
// Source: docs/aetherarray-master-reference.md, block `stackup:begin pointing`, itself
// generated from hardware/rev-a/stackup/reva-stackup.json by
// `python -m rfkit.cli stackup --write-docs` (run from tools/).
// Regenerate with: python tools/docs/md_to_typst.py --generated

#import "../template.typ": *

Keeping the 315 degree state within 2.29 degrees needs the beamformer substrate permittivity known to plus or minus 0.073, about 1.7 per cent.

#table(
  columns: (1.2fr, 1.2fr, 2.1fr, 1.8fr),
  table.header([Steering angle (deg)], [Pointing budget (deg)], [Shift, permittivity bound alone, phase scaled by 2.01 per cent (deg)], [Shift, worst corner, phase scaled by 3.67 per cent (deg)]),
  [0], [0.585], [0.000], [0.000],
  [15], [0.605], [0.654], [1.191],
  [30], [0.675], [0.668], [1.221],
  [45], [0.827], [0.194], [0.354],
)

Shift is the worst over the eight command origins, from `rfkit.budget.worst_proportional_pointing_deg`; the budget is decision 0007's pointing bound at that angle.
