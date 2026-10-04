// GENERATED FILE, do not edit by hand.
// Source: docs/aetherarray-master-reference.md, block `stackup:begin seeds`, itself
// generated from hardware/rev-a/stackup/reva-stackup.json by
// `python -m rfkit.cli stackup --write-docs` (run from tools/).
// Regenerate with: python tools/docs/md_to_typst.py --generated

#import "../template.typ": *

*INITIALISATION ONLY.* $W_"seed" eq.not W_50$. SIM-001 decides the width; every length below is a feasibility estimate, not a layout value.

#table(
  columns: (auto, 1.5fr, auto),
  table.header([Construction], [Quantity], [Value]),
  [beamformer], [$W_"seed"$ for 50 ohm], [0.372 mm],
  [beamformer], [closed form check, zero thickness], [0.402 mm],
  [beamformer], [$epsilon_"eff"$ at $f_0$], [3.191],
  [beamformer], [$lambda_0$], [122.9 mm],
  [beamformer], [$lambda_g$], [68.8 mm],
  [beamformer], [line for 45 degrees], [8.6 mm],
  [beamformer], [line for 90 degrees], [17.2 mm],
  [beamformer], [line for 180 degrees], [34.4 mm],
  [beamformer], [line for 315 degrees], [60.2 mm],
  [beamformer], [$W_"seed"$ for 70.7 ohm, Wilkinson arms], [0.182 mm],
  [beamformer], [width flags], [none],
  [antenna], [$W_"seed"$ for 50 ohm], [2.836 mm],
  [antenna], [closed form check, zero thickness], [2.876 mm],
  [antenna], [$epsilon_"eff"$ at $f_0$], [3.415],
  [antenna], [$lambda_0$], [122.9 mm],
  [antenna], [$lambda_g$], [66.5 mm],
  [antenna], [line for 45 degrees], [8.3 mm],
  [antenna], [line for 90 degrees], [16.6 mm],
  [antenna], [line for 180 degrees], [33.2 mm],
  [antenna], [line for 315 degrees], [58.2 mm],
  [antenna], [width flags], [none],
)
