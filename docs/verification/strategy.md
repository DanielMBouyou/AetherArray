# How we know a result is right

- Status: in progress
- Last reviewed: 2026-08-21

## 1. Checking the simulator

The simulator underpins the whole theoretical track. If it is wrong, everything is.

| Check | Expected value |
| --- | --- |
| Pattern with no defects, uniform array | beam width and side lobe level matching the classical formulas |
| Array with a single element | the single element pattern, with no array directivity |
| Broadside pointing requested | maximum exactly at zero |
| Thirty degree pointing requested | maximum at thirty degrees, to numerical precision |
| Spacing beyond half a wavelength | a grating lobe appears, at the predicted position |
| Zero phase errors | result identical to the ideal case |

These checks are quick to write and catch nearly every implementation error.

## 2. Checking the calibration methods

| Check | Method |
| --- | --- |
| With no noise, does the method recover the injected defects exactly? | simulation, direct comparison |
| With zero defect, does the method return a zero correction? | control case |
| Does quality degrade smoothly as noise rises? | sweep |
| Does the result depend on the order of the measurements? | permutation |

The first is the most important. A method that fails to recover the truth in the
absence of noise is wrong, and no amount of tuning will save it.

## 3. Checking the real measurement

| Check | What it catches |
| --- | --- |
| Repeated measurement with nothing touched | measurement noise |
| Repeated measurement after reassembly | mechanical repeatability |
| Measurement with a single element driven | single element behaviour, a reference |
| Measurement with the array physically flipped | asymmetry of the bench or the environment |
| Verifying the effect of a known error | full validation of the chain |

The fourth is a neat trick: if you physically flip the array, the measured pattern
should be the mirror image of the previous one. If it is not, what you are seeing is
the environment, not the array.

The last corresponds to EXP-007. It validates the array, the measurement bench and
the theory at once, which makes it the highest value experiment in the project.

## 4. Checking a conclusion before publishing it

- [ ] Is the observed gap larger than the repeated measurement noise?
- [ ] Are the measurement conditions recorded, including the environment?
- [ ] Is the number of measurements consumed stated?
- [ ] Was the comparison repeated over several draws or several sessions?
- [ ] Are simulation and measurement results clearly distinguished?

## 5. What is not planned

- No anechoic chamber measurement, unless an opportunity appears.
- No full near field scan, unless a precise positioner becomes available.
- No cross polarisation characterisation in the first phase.
