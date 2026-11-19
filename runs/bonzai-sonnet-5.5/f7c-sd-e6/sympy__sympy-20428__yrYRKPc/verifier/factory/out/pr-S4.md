Strip zero leading coefficients in dup_mul_ground/dmp_mul_ground (fixes unstripped DMP from clear_denoms)

## Overview
`Poly.clear_denoms()` on a constant over `EX` that is zero but not yet simplified to zero returned a polynomial that printed as `Poly(0, x, domain='EX')` but whose rep was `[EX(0)]` instead of `[]`. `is_zero`, `degree()` and leading-coefficient code treated it as non-zero, which caused the `ZeroDivisionError` in #17990.

## Details
`dup_clear_denoms`/`dmp_clear_denoms` multiply by the common denominator with `dup_mul_ground`/`dmp_mul_ground`, which never stripped. In `EX`, `EX.__mul__` simplifies the product, so an element that was truthy before (`bool(EX(expr)) is True`) becomes `EX(0)` after, leaving a leading zero. The fix strips the result in `dup_mul_ground` (`dup_strip`) and `dmp_mul_ground` (`dmp_strip`, with the recursion stripping inner levels), which is where the invariant is broken, so every caller is covered, not only clear_denoms.

Tests added: `test_clear_denoms_strips_zero` (densetools) and an extra case in `test_Poly_clear_denoms` (polytools) using `1/(1 + sqrt(2)) - (sqrt(2) - 1)`. Both failed before the change (`dup_clear_denoms([zero], EX)[1]` was `[EX(0)]`).

## Verification
- `python bin/test sympy/polys/tests/test_densetools.py sympy/polys/tests/test_polytools.py -k clear_denoms`: 5 passed (2 failed before).
- `python bin/test sympy/polys sympy/solvers/tests/test_polysys.py`: all passed.
- `python bin/doctest sympy/polys/densearith.py sympy/polys/densetools.py`: 98 passed.
