// GENERATED FILE, do not edit by hand.
// Source: docs/aetherarray-master-reference.md, block `stackup:begin comparison`, itself
// generated from hardware/rev-a/stackup/reva-stackup.json by
// `python -m rfkit.cli stackup --write-docs` (run from tools/).
// Regenerate with: python tools/docs/md_to_typst.py --generated

#import "../template.typ": *

#landscape-table[
#table(
  columns: (2.4fr, 4.1fr, auto, auto, auto, auto, auto, 2.1fr, 1.7fr, 2.0fr, 1.8fr),
  table.header([Construction], [Process], [$h$ (mm)], [$epsilon_r$, status], [$tan delta$], [$W_"seed"$ (mm)], [$lambda_g$ (mm)], [315 degree loss spread, smooth to doubled conductor loss (dB)], [315 degree error from the $epsilon_r$ bound (deg)], [Patch bandwidth, efficiency], [Width flags]),
  [beamformer, selected], [JLCPCB, 4 layer FR-4, 1.6 mm, controlled impedance stack-up JLC04161H-7628], [0.210], [4.4, nominal], [0.015], [0.372], [68.8], [0.59 to 0.86], [6.3, assumed], [0.14 per cent, 9 per cent], [none],
  [antenna, selected], [JLCPCB, 2 layer FR-4, 1.6 mm, 1 oz finished copper], [1.530], [4.5, nominal], [0.015], [2.836], [66.5], [0.36 to 0.39], [9.8, assumed], [1.05 per cent, 48 per cent], [none],
  [ro4350b\_thin\_2l, candidate], [JLCPCB, 2 layer RO4350B, 0.51 mm core, finished 0.6 mm, 1 oz, ENIG], [0.508], [3.66, typical], [0.0031], [1.073], [73.2], [0.17 to 0.27], [1.9, guaranteed], [0.39 per cent, 49 per cent], [wide: over the SC-70-6 lead pitch, a taper at every switch pin],
  [ro4350b\_thick\_2l, candidate], [JLCPCB, 2 layer RO4350B, 1.52 mm core, finished 1.65 mm, 1 oz, ENIG], [1.524], [3.66, typical], [0.0031], [3.291], [72.5], [0.10 to 0.13], [1.9, guaranteed], [1.18 per cent, 81 per cent], [none],
  [fr408hr\_4l, candidate], [OSH Park, 4 layer FR408HR, 1.6 mm, ENIG], [0.200], [3.61, typical], [0.009], [0.405], [74.7], [0.46 to 0.73], [3.0, assumed], [0.15 per cent, 12 per cent], [none],
)
]
