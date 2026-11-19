Raise PolynomialError from apart() for non-rational commutative input

## Overview
`apart(sin(x)/(x + 1), x)` and `apart(1/(x**y + 1), x)` returned the input unchanged with no error, instead of raising `PolynomialError` as released sympy does. Callers that relied on the validation error got a silent success. `apart()` now raises again; rational functions decompose as before.

## Details
In `sympy/polys/partfrac.py`, the `except PolynomialError` branch returned `f` for commutative input; it now re-raises (`raise PolynomialError(msg)`). The non-commutative handling is unchanged.

Test: `test_apart` in `sympy/polys/tests/test_partfrac.py` now asserts `PolynomialError` for both inputs (failed with "DID NOT RAISE" before the fix).

## Verification
- `python -m pytest sympy/polys/tests/test_partfrac.py` (fails before, passes after)
- `python -m pytest sympy/polys sympy/integrals/tests/test_rationaltools.py sympy/integrals/tests/test_risch.py`: 996 passed
