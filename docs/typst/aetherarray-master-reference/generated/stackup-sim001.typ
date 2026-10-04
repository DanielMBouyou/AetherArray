// GENERATED FILE, do not edit by hand.
// Source: docs/aetherarray-master-reference.md, block `stackup:begin sim001`, itself
// generated from hardware/rev-a/stackup/reva-stackup.json by
// `python -m rfkit.cli stackup --write-docs` (run from tools/).
// Regenerate with: python tools/docs/md_to_typst.py --generated

#import "../template.typ": *

Generated from `reva-stackup-r1:6363d8ab0f2b`, construction `beamformer`. *$W_"seed"$ is not the final width.*

#table(
  columns: (auto, 1.0fr, 2.3fr),
  table.header([Variable], [Value], [Origin]),
  [`sub_h`], [0.2104 mm], [PP1 thickness],
  [`cu_t`], [0.035 mm], [L1 finished copper],
  [`w_seed`], [0.372 mm], [50 ohm seed, scikit-rf model],
  [`l_short`], [10 mm], [fixed choice],
  [`l_long`], [27.2 mm], [short line plus a quarter guided wavelength at $f_0$],
  [`port_w`], [3.72 mm], [the larger of ten widths and the width plus ten heights],
  [`port_h`], [2.104 mm], [ten substrate heights],
  [`sub_er`], [4.4], [PP1 permittivity, nominal],
  [`sub_tand`], [0.015], [PP1 loss tangent],
  [`cu_sigma`], [5.8e+07 S/m], [copper, assumed],
  [width sweep], [0.3348, 0.372, 0.4092 mm], [the seed scaled by 0.9, 1.0 and 1.1],
)

Solution frequency 2.44 GHz; sweep 1 to 3 GHz in 5 MHz steps; maximum change in S 0.02 over 2 consecutive passes, at most 20 passes; ports renormalised to 50 ohm.
