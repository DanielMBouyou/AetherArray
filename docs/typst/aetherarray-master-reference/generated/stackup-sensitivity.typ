// GENERATED FILE, do not edit by hand.
// Source: docs/aetherarray-master-reference.md, block `stackup:begin sensitivity`, itself
// generated from hardware/rev-a/stackup/reva-stackup.json by
// `python -m rfkit.cli stackup --write-docs` (run from tools/).
// Regenerate with: python tools/docs/md_to_typst.py --generated

#import "../template.typ": *

Each bound applied alone at the seed width, then the worst of every corner. Phase is the error of a line laid out for the nominal permittivity.

#small-table[
#table(
  columns: (auto, 1.8fr, auto, auto, 1.1fr, 1.1fr),
  table.header([Construction], [Tolerance], [Status], [$Z_0$ (ohm)], [180 degree error (deg)], [315 degree error (deg)]),
  [beamformer], [rf dielectric thickness], [assumed], [46.9 to 52.8], [+0.76 to -0.67], [+1.34 to -1.16],
  [beamformer], [rf dielectric permittivity], [assumed], [51.0 to 49.0], [-3.62 to +3.55], [-6.34 to +6.21],
  [beamformer], [rf copper thickness], [assumed], [50.0 to 49.7], [+0.00 to -0.37], [+0.00 to -0.65],
  [beamformer], [etched width], [guaranteed], [56.3 to 45.0], [-2.10 to +1.78], [-3.68 to +3.12],
  [beamformer], [worst corner of the bounds above], [combined], [41.1 to 60.5], [6.60], [11.56],
  [antenna], [rf dielectric thickness], [assumed], [46.9 to 52.9], [+0.70 to -0.60], [+1.22 to -1.05],
  [antenna], [rf dielectric permittivity], [assumed], [51.6 to 49.5], [-5.57 to +1.82], [-9.75 to +3.19],
  [antenna], [etched width], [guaranteed], [56.7 to 44.8], [-1.90 to +1.63], [-3.33 to +2.86],
  [antenna], [rf copper thickness], [unbounded], [not computed], [not computed], [not computed],
  [antenna], [worst corner of the bounds above], [combined], [41.4 to 61.6], [7.88], [13.80],
)
]
