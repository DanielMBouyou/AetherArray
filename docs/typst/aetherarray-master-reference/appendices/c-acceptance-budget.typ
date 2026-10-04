#import "../template.typ": *

== Appendix C. RF acceptance budget

#table(
  columns: (2.5fr, 3.7fr, 1.3fr),
  table.header([Item], [Value], [Record]),
  [quantisation floor], [12.99 degrees rms; 1.85 degrees pointing at broadside; 0.167 dB gain; $- 18.9$ dB error sidelobe floor], [decision 0007],
  [policy fraction], [$eta = 0.10$, declared], [decision 0007],
  [pointing budget at broadside], [0.585 degrees], [`python -m rfkit.cli budget`],
  [HFSS against ADS, $S_21$ phase, state dependent], [2.29 degrees], [decision 0007],
  [HFSS against ADS, $S_21$ magnitude, state dependent], [0.40 dB], [decision 0007],
  [amplitude imbalance, one array state], [0.82 dB peak to peak], [decision 0007],
  [hardware state dependent phase against nominal], [2.29 degrees at $f_0$, a derived requirement, not wired], [decision 0007],
  [simulation against analyser], [unresolved until the analyser's $U$ is known], [decision 0007],
  [solver convergence for a comparison], [$Delta S lt.eq abs(S_21) thin T$, about $0.04 thin abs(S_21)$], [decision 0007],
  [coupling allocation], [$eta_c = 0.10$, separate; together at most 0.20 of the floor variance], [decision 0008],
  [coupling screen, descriptive only], [$rho lt.eq 0.040$: about $- 28$ dB aggregate, $- 34$ dB per neighbour], [decision 0008],
  [how values may change], [only by a new decision with a derivation input change; never from the judged discrepancies], [decision 0007],
)
