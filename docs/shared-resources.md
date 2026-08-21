# What this project shares with the others

- Status: observing
- Last reviewed: 2026-08-21

## Strong link with the RF modelling project

Both use the same instruments, the same instrument calibration method, the same
connectors, and probably the same board fabricator.

| Shared element | Nature | Recommendation |
| --- | --- | --- |
| Vector network analyser | single physical resource | occupancy calendar |
| Instrument calibration procedure | identical method | write it once, reference it from both repositories |
| Instrument automation | same approach, same library | accepted duplication at first, extraction later |
| S parameter processing | same tooling | same |
| Cables, attenuators, adapters | physical resources | a shared inventory is useful |
| Board orders | significant fixed setup costs | group the orders |
| Electromagnetic simulation and scripting | same tools, different structures | share the method, not the models |
| Angular positioner | useful to both | design once, with both uses in mind |

The last row is a rare case of obvious hardware sharing. A positioner driven by a
microcontroller serves pattern measurement here and repeatable measurement there.

## Conditional link with the FPGA projects

An FPGA only enters this project if the digital architecture is chosen. In that case
two skills become directly shared:

| Element | Source project | Use here |
| --- | --- | --- |
| Precise synchronisation between boards | muMarket | coherence between receive channels |
| Fixed point digital signal processing | FlowTensor | embedded beamforming |
| RTL test benches | NeuroVerify-SoC | verifying the processing |

If the analogue architecture is chosen, that link disappears, and it should be
accepted rather than forced.

## Shared hardware

| Resource | Shared with | Conflict | Handling |
| --- | --- | --- | --- |
| Network analyser | NeuralRFIC | yes, strongly | calendar |
| Oscilloscope | all | yes | calendar |
| FPGA boards | muMarket, FlowTensor, NeuroVerify-SoC | only on the digital route | to arbitrate |
| Microcontrollers | all | low | positioner and phase shifter control here |
| Gaming PC | FlowTensor, NeuralRFIC | low here | queue |

## What must not be shared

- The array calibration algorithms, which are specific.
- The array simulator.
- The pattern metrics.

## Scheduling note

This project and the RF modelling project compete for the same main instrument.
Running them strictly in parallel would create constant blocking, since a calibrated
setup cannot be dismantled between sessions without losing the calibration.
Alternating by phase is the sensible arrangement.
