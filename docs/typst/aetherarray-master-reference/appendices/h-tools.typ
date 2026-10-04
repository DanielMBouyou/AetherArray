#import "../template.typ": *

== Appendix H. Software and tool index

#table(
  columns: (1.8fr, 5.9fr),
  table.header([Item], [Path]),
  [RF data layer], [`tools/rfkit/`, with `tools/rfkit/README.md`],
  [tests], [`tools/rfkit/tests/`],
  [SIM-001 builder and analysis], [`tools/sim/sim001_hfss.py`, `tools/sim/sim001_analyse.py`],
  [runbook builder], [`tools/runbooks/build.py`],
  [documentation checks], [`tools/check-docs.sh`],
  [schematic generator], [`hardware/rev-a/tools/generate-schematic.py`],
  [figures of this document], [`tools/docs/master_reference_figures.py`, output in `docs/figures/`],
  [CI workflows], [`.github/workflows/`],
  [package list], [`requirements.txt`],
)

Part XII gives each tool's role and status.
