Strip leading zeros in dup_mul_ground/dmp_mul_ground (fixes unstripped zero from clear_denoms)

## Overview
`Poly.clear_denoms()` could return a polynomial whose representation was `DMP([EX(0)], EX, None)` instead of the canonical `DMP([], EX, None)`. It printed like zero but `is_zero` was False and `terms_gcd()`/`primitive()` misbehaved, which was the immediate cause of the `ZeroDivisionError` in #17990. The ground-multiplication helpers now strip the result.

## Details
With an `EX` domain a coefficient may not simplify to 0 until it is multiplied by the common denominator. `dup_clear_denoms`/`dmp_clear_denoms` multiply through `dup_mul_ground`/`dmp_mul_ground`, which returned the product list without stripping leading zeros. Fix: `dup_mul_ground` returns `dup_strip(...)` and `dmp_mul_ground` returns `dmp_strip(..., u)`.

Regression test in `test_Poly_clear_denoms` uses `e = 1/(1+sqrt(2)) - sqrt(2) + 1` with `Poly(e*x + e, x, domain='EX')`. Before: rep `[EX(0), EX(0)]`, `is_zero` False. After: rep `[]`, `is_zero` True, `terms_gcd()` works.

## Verification
- New test failed before the fix, passes after.
- `pytest sympy/polys sympy/integrals/tests/test_risch.py`: 985 passed, 3 xfailed, 1 xpassed.
- Doctests of densearith.py and densetools.py pass.
