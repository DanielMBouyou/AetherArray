// GENERATED FILE, do not edit by hand.
// Source: docs/aetherarray-master-reference.md, block `stackup:begin patch`, itself
// generated from hardware/rev-a/stackup/reva-stackup.json by
// `python -m rfkit.cli stackup --write-docs` (run from tools/).
// Regenerate with: python tools/docs/md_to_typst.py --generated

#import "../template.typ": *

*SANITY CHECK ONLY.* The patch length, width, feed and spacing stay free parameters for HFSS. These figures only say whether a patch is physically sensible on each construction.

#small-table[
#table(
  columns: (auto, auto, auto, 1.5fr, 1.5fr, 2.4fr),
  table.header([Construction], [$W_p$ (mm)], [$L_p$ (mm)], [Bandwidth, VSWR 2], [Radiation efficiency], [Resonance shift over the permittivity bound]),
  [beamformer], [37.4], [29.3], [0.14 per cent], [9 per cent], [-2.19 to +2.34 per cent],
  [antenna], [37.0], [28.6], [1.05 per cent], [48 per cent], [-1.06 to +3.38 per cent],
)
]

Four elements at half a free space wavelength need an antenna board about 260 mm long, sanity check only.
