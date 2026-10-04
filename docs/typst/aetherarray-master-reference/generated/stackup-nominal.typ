// GENERATED FILE, do not edit by hand.
// Source: docs/aetherarray-master-reference.md, block `stackup:begin nominal`, itself
// generated from hardware/rev-a/stackup/reva-stackup.json by
// `python -m rfkit.cli stackup --write-docs` (run from tools/).
// Regenerate with: python tools/docs/md_to_typst.py --generated

#import "../template.typ": *

*beamformer*, RF beamformer and control interface board: JLCPCB, 4 layer FR-4, 1.6 mm, controlled impedance stack-up JLC04161H-7628.

#small-table[
#table(
  columns: (auto, 2.2fr, 3.1fr, auto, auto, auto),
  table.header([Layer], [Material], [Role], [Thickness], [Status], [Source]),
  [L1], [copper], [RF microstrip, RF components, local escapes outside RF keep-out], [0.035 mm], [nominal], [V8],
  [PP1], [fr4\_prepreg\_7628], [RF substrate], [0.2104 mm], [nominal], [V8],
  [L2], [copper], [continuous RF reference plane, no routing, no splits], [0.0152 mm], [nominal], [V8],
  [CORE], [fr4\_core\_np155f], [core], [1.065 mm], [nominal], [V8],
  [L3], [copper], [power rails and slow digital: beam state lines, strobe, I2C, converter], [0.0152 mm], [nominal], [V8],
  [PP2], [fr4\_prepreg\_7628], [lower prepreg], [0.2104 mm], [nominal], [V8],
  [L4], [copper], [digital and connector routing, ground pour stitched to L2], [0.035 mm], [nominal], [V8],
)
]

*antenna*, four element antenna array board: JLCPCB, 2 layer FR-4, 1.6 mm, 1 oz finished copper.

#small-table[
#table(
  columns: (auto, auto, 2.4fr, auto, auto, auto),
  table.header([Layer], [Material], [Role], [Thickness], [Status], [Source]),
  [L1], [copper], [patches, feed lines, SMA launches], [0.035 mm], [nominal], [V11],
  [CORE], [fr4\_two\_layer], [RF substrate], [1.53 mm], [assumed], [D0009],
  [L2], [copper], [continuous ground under every patch and feed, no routing], [0.035 mm], [nominal], [V11],
)
]

#table(
  columns: (2.2fr, 5.7fr),
  table.header([Material], [Designation]),
  [copper], [electrodeposited copper, foil type not published by the fabricator],
  [fr4\_prepreg\_7628], [7628 glass prepreg, resin content 49 per cent, in the fabricator's NP-155F based stack-up; brand not guaranteed per order],
  [fr4\_core\_np155f], [NP-155F core assumed by the fabricator's calculator],
  [fr4\_two\_layer], [two layer FR-4 core; brand not fixed by the fabricator, one of NP-140F, KB-6164, S1141 or S1000H (V14)],
  [lpi\_soldermask], [liquid photoimageable solder mask],
)

#small-table[
#table(
  columns: (2.2fr, auto, auto, auto, auto, 3.8fr),
  table.header([Material], [Property], [Value], [Status], [Source], [Frequency and method]),
  [copper], [conductivity], [5.8e+07 S/m], [assumed], [D0009], [not applicable],
  [fr4\_prepreg\_7628], [permittivity], [4.4], [nominal], [V8], [not stated; fabricator impedance calculator value, no frequency stated],
  [fr4\_prepreg\_7628], [loss tangent], [0.015], [typical], [V12], [1 GHz; IPC-TM-650 2.5.5.9],
  [fr4\_core\_np155f], [permittivity], [4.6], [nominal], [V8], [not stated; fabricator impedance calculator value, no frequency stated],
  [fr4\_core\_np155f], [loss tangent], [0.015], [typical], [V12], [1 GHz; IPC-TM-650 2.5.5.9],
  [fr4\_two\_layer], [permittivity], [4.5], [nominal], [V11], [not stated; fabricator capability page value for two layer boards, no frequency stated],
  [fr4\_two\_layer], [loss tangent], [0.015], [assumed], [D0009], [not stated],
  [lpi\_soldermask], [permittivity], [3.8], [nominal], [V8], [not stated; fabricator impedance calculator value],
)
]
