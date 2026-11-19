Fix refraction_angle/deviation reporting 0 for total internal reflection with an angle input

## Overview
For a plain incidence angle above the critical angle (e.g. glass to air at a steep angle), `refraction_angle` returned `0`, which is also the correct answer for normal incidence, and `deviation` turned it into `-incidence_angle`. The calculator therefore showed a zero-degree outgoing ray instead of "unavailable".

## Details
- `refraction_angle` now raises `TotalInternalReflectionError` (a `ValueError` subclass, message "Ray undergoes total internal reflection") for angle input above the critical angle. Ray/vector input is unchanged (still returns 0).
- `deviation` catches that specific error and returns `None`, matching its existing ray-input TIR behaviour. Other ValueErrors (e.g. angle out of range) still propagate.
- Docstrings updated; tests added in `sympy/physics/optics/tests/test_utils.py`.

## Verification
`pytest sympy/physics/optics` (16 passed); doctests of `utils.py` pass. The new tests fail on the base commit.
