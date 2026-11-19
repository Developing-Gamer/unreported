Strip leading zeros in dup_mul_ground/dmp_mul_ground (fixes unstripped result of clear_denoms)

## Problem
`Poly.clear_denoms()` on an `EX`-domain poly whose coefficient is zero but not recognised as such (e.g. the huge constant in the issue, which led to the `ZeroDivisionError` in #17990) returned `DMP([EX(0)], EX, None)`. It prints like the zero poly, but `is_zero` is `False`, and `terms_gcd()` raises `IndexError: tuple index out of range` (`monomial_min`).

## Cause
`dup_clear_denoms`/`dmp_clear_denoms` multiply every coefficient by the common denominator via `dup_mul_ground`/`dmp_mul_ground`, which did not strip the result. With `EX`, a coefficient that is not detected as zero can become exactly zero after multiplication, leaving a non-canonical unstripped representation.

## Fix
`dup_mul_ground` now returns `dup_strip([cf*c ...])` and `dmp_mul_ground` returns `dmp_strip([...], u)`, so the result is always canonical.

## Verification
- New regression test in `test_Poly_clear_denoms` (smaller expression `1/(1+sqrt(2)) - sqrt(2) + 1`, halved, in `EX`): fails before (`assert [EX(0)] == []`), passes after.
- `pytest sympy/polys sympy/solvers/tests/test_polysys.py`: 954 passed, 3 xfailed, 1 xpassed.
