// GENERATED FILE, do not edit by hand.
// Source: docs/aetherarray-master-reference.md, block `stackup:begin tolerances`, itself
// generated from hardware/rev-a/stackup/reva-stackup.json by
// `python -m rfkit.cli stackup --write-docs` (run from tools/).
// Regenerate with: python tools/docs/md_to_typst.py --generated

#import "../template.typ": *

#small-table[
#table(
  columns: (auto, 1.7fr, auto, 1.8fr, auto, auto),
  table.header([Construction], [Tolerance], [Input], [Bound], [Status], [Source]),
  [beamformer], [rf dielectric thickness], [$h$], [minus 10 to plus 10 per cent], [assumed], [V11],
  [beamformer], [rf dielectric permittivity], [$e r$], [minus 0.2 to plus 0.2], [assumed], [D0009],
  [beamformer], [rf copper thickness], [$t$], [minus 0 to plus 0.0056 mm], [assumed], [V9],
  [beamformer], [etched width], [$w$], [minus 20 to plus 20 per cent], [guaranteed], [V11],
  [antenna], [rf dielectric thickness], [$h$], [minus 10 to plus 10 per cent], [assumed], [V11],
  [antenna], [rf dielectric permittivity], [$e r$], [minus 0.3 to plus 0.1], [assumed], [D0009],
  [antenna], [rf copper thickness], [$t$], [unbounded, no number], [unbounded], [V11],
  [antenna], [etched width], [$w$], [minus 20 to plus 20 per cent], [guaranteed], [V11],
)
]
