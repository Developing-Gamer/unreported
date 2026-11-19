apart(): raise PolynomialError for non-rational commutative input instead of returning it unchanged

## Overview
`apart(1/(sin(x) + 1), x)` (and similar fractions containing `sin`, `exp`, ...) returned the input exactly as entered with no error, instead of the `PolynomialError` validation failure callers used to get. Ordinary rational functions never reach that branch, so they were unaffected.

## Details
In `sympy/polys/partfrac.py`, the `except PolynomialError` handler in `apart()` did `return f` for commutative expressions, swallowing the failure from `parallel_poly_from_expr`. It now re-raises `PolynomialError(msg)`. The non-commutative handling below it is unchanged. Existing callers (e.g. `sympy/concrete/summations.py`) already catch `PolynomialError` around `apart`.

Regression test `test_apart_non_polynomial` added in `sympy/polys/tests/test_partfrac.py`.

## Verification
- `python bin/test sympy/polys/tests/test_partfrac.py` fails on the base commit with `Failed: DID NOT RAISE` and passes with the fix.
- Caller test suites (integrals, series, simplify, core expr, ode) run as well.
