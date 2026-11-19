Fix unstripped zero DMP from Poly.clear_denoms with EX coefficients

Root cause: `ExpressionDomain.Expression.__bool__` returned `f.ex != 0`, a structural comparison. After `clear_denoms` multiplies EX coefficients, a coefficient that is mathematically zero but not syntactically `0` is truthy, so `dup_mul_ground`/`dup_strip` do not strip it. The result prints as `Poly(0, x, domain='EX')` but has rep `DMP([EX(0)], EX)`, so `is_zero` is False and `terms_gcd()` raises IndexError (and `primitive()` once raised ZeroDivisionError, see #17990).

Change: `__bool__` now returns `not f.ex.is_zero`, so zero-valued EX elements are falsy and get stripped. Unknown (`None`) zero-ness still counts as nonzero. Added a regression test to `test_Poly_clear_denoms` using the expression from the issue.

Verification: `python bin/test sympy/polys` passes (944 passed; the one xpass in test_partfrac is pre-existing). The issue example now gives rep `DMP([], EX, None)`, `is_zero` True, and `terms_gcd()` returns `((0,), Poly(0, x, domain='EX'))`.
