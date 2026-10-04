#import "../template.typ": *

== Appendix G. Decision index

#table(
  columns: (auto, 4.1fr, 3.6fr),
  table.header([ID], [Title], [Status]),
  [0001], [build the simulator before the array], [accepted],
  [0002], [learning enters as a drift prior, not as a first calibration shortcut], [accepted, four gates named],
  [0003], [Rev A is a two board, phase only, switched line array at three bits], [accepted; control path superseded by 0005],
  [0004], [the working frequency is 2.44 GHz], [accepted],
  [0005], [the Rev A controller is an external DE1-SoC], [accepted; re-capture required],
  [0006], [purchases are staged by what they unblock], [accepted],
  [0007], [a provisional RF acceptance budget from the quantisation floor], [accepted; values provisional-theory-derived],
  [0008], [gate G4: the diagonal state stays only if neglecting coupling costs less than the budget], [accepted; no data],
  [0009], [the Rev A stack-up], [accepted],
)
