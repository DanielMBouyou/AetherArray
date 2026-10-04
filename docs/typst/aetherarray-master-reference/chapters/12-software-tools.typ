#import "../template.typ": *

= Part XII. Software and tool table <part-xii-software-and-tool-table>

Only tools the project uses, has decided to use, or has explicitly not chosen are listed.

#small-table[
#table(
  columns: (57pt, 3.4fr, 2.9fr, 53pt, 46pt, 68pt, 2.7fr),
  table.header([Tool], [Role], [Why this tool], [Input], [Output], [Alternative], [Status, 2026-10-04]),
  [Python 3.12], [working language of analysis, scripting, tests], [one language from solver scripting to inference; free], [data, configs], [results, figures], [MATLAB, listed in the inventory as a cross check], [in use; pinned in CI],
  [NumPy, SciPy], [arrays, root finding, statistics], [the base of scikit-rf; standard], [numbers], [numbers], [none needed], [pinned],
  [scikit-rf], [common RF data layer: Touchstone, networks, line models], [open, tested, reads every source's files], [`.sNp` files, line parameters], [`Network` objects, seeds], [vendor tools' own analysis], [pinned 1.12.0],
  [rfkit], [project specific metrics, comparisons, array state, budget, G4, stack-up], [encodes the comparison rules once, with tests], [traces with provenance, canonical stack-up], [verdicts, array states, generated tables], [ad hoc notebooks], [implemented; 160 tests; synthetic data only],
  [HFSS Student], [geometry aware full wave validation, locally], [default HFSS path within documented limits], [geometry, materials, ports], [`.s2p`, `.s4p`, fields, patterns], [full HFSS; a free full wave solver as a cross check (state of the art O4)], [installed 2025 R2; *no successful solve*],
  [full HFSS], [the same, beyond the Student limits], [only on escalation], [as above], [as above], [none], [at school; not needed so far],
  [PyAEDT], [scripted model building from the canonical stack-up], [reproducibility, no retyping], [canonical stack-up], [HFSS projects, exports, sidecars], [building by hand], [builder written; dry run in CI; not executed successfully],
  [ADS], [independent circuit and distributed model], [different model form from HFSS, for decision 0007's comparison], [line models, component S-parameters], [`.s2p`], [scikit-rf media locally], [at school, optional; *no model exists*],
  [KiCad], [schematic capture], [free; scriptable symbol and sheet files], [the generator script], [schematic, BOM, ERC report], [none considered], [schematic captured; ERC clean; version 10 expected],
  [Git and GitHub], [version control, timestamps for pre-registration], [the commit is the evidence of when a rule was written], [everything], [history], [none], [in use],
  [GitHub Actions], [continuous checks], [runs on every push], [repository], [pass or fail], [none], [three workflows: docs, rf, runbooks],
  [Quartus], [DE1-SoC FPGA toolchain], [the vendor tool for the Cyclone V], [gateware sources], [bitstream], [none for this device], [17.1 installed; no gateware; no programmer attached],
  [DE1-SoC FPGA and HPS], [deterministic timing and control, not learning; storage and inference on the HPS], [decision 0005], [sequences], [applied states, records], [a microcontroller, option A of decision 0005], [owned; nothing implemented],
  [R&S ZVL analyser], [every real RF measurement: complex S-parameters], [the observed instrument; reaches 2.44 GHz with phase], [the device, at calibrated planes], [Touchstone files], [the documented FieldFox, if present], [*\[observed\]*; model, kit, options unconfirmed],
  [Touchstone], [the bridge between every tool], [universal text format], [any S-parameter source], [`.sNp`], [vendor binary formats], [the chosen exchange format],
  [matplotlib, reportlab, mistune, pillow, pymupdf], [figures; runbook PDFs], [deterministic, scriptable], [Markdown, data], [PDFs, figures], [none], [pinned; runbook SCH-001 built],
  [scikit-learn, PyTorch], [possible learning libraries], [not chosen], [], [], [], [*not dependencies*; the model class is chosen on data],
  [Gaussian process or Kalman filter tooling], [the drift prior], [candidates in section 40], [], [], [], [*not chosen*],
)
]
