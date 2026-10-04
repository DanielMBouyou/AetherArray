#import "../template.typ": *

== Appendix A. Rev A parameters

Decided parameters, each from its record:

#table(
  columns: (1.5fr, 2.4fr, 5.7fr),
  table.header([Parameter], [Value], [Source]),
  [element count], [4], [decision 0003],
  [working frequency], [2.44 GHz, band 57a, 2400 to 2483.5 MHz], [decision 0004],
  [free space wavelength], [122.9 mm], [from $f_0$],
  [element spacing], [$lambda_0 \/ 2$, 61.4 mm], [decisions 0003, 0004],
  [aperture across element centres], [184 mm], [EXP-004],
  [far field distance], [0.55 m], [EXP-004],
  [phase bits], [45, 90, 180 degrees, eight states], [decision 0003],
  [relative beam states], [512; 820 with enable bits], [section 8.3],
  [amplitude control], [none; enable or terminate per channel], [decision 0003],
  [RF switches], [29 PE4259-63: 28 in the channels, 1 path selector], [`hardware/rev-a/README.md`],
  [divider], [four way Wilkinson, three stages, 70.7 ohm arms, 100 ohm resistors], [`hardware/rev-a/layout-constraints.md`],
  [detector], [AD8318, $- 25$ mV/dB nominal], [decision 0003, V6],
  [temperature sensors], [two MCP9808 at 0x18 and 0x19, plus the AD8318 die output], [decision 0003],
  [controller], [external DE1-SoC], [decision 0005],
  [beam state word], [16 bits, $b = 4 c + f$], [`docs/architecture/control-architecture.md`],
  [stack-up], [`reva-stackup-r1`], [decision 0009],
  [acceptance policy], [$eta = 0.10$; $eta_c = 0.10$ for coupling], [decisions 0007, 0008],
)

Derived dimensions, generated, *not layout values*:

#include "../generated/stackup-seeds.typ"

SIM-001 inputs, generated:

#include "../generated/stackup-sim001.typ"
