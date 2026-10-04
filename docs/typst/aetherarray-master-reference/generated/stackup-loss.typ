// GENERATED FILE, do not edit by hand.
// Source: docs/aetherarray-master-reference.md, block `stackup:begin loss`, itself
// generated from hardware/rev-a/stackup/reva-stackup.json by
// `python -m rfkit.cli stackup --write-docs` (run from tools/).
// Regenerate with: python tools/docs/md_to_typst.py --generated

#import "../template.typ": *

#table(
  columns: (auto, 1.4fr, 1.5fr, 2.0fr, 1.4fr),
  table.header([Construction], [Conductor loss (dB/m)], [Dielectric loss (dB/m)], [Extra loss of the 315 degree state, smooth copper (dB)], [Same, conductor loss doubled (dB)]),
  [beamformer], [4.49], [5.29], [0.59], [0.86],
  [antenna], [0.59], [5.60], [0.36], [0.39],
)
