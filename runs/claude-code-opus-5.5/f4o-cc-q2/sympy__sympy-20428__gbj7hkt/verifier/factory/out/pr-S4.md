Strip zero coefficients in dup_mul_ground/dmp_mul_ground (fixes unstripped DMP from clear_denoms)

## Root cause

`Poly.clear_denoms()` calls `dmp_clear_denoms`, which multiplies every coefficient by the
common denominator using `dup_mul_ground` / `dmp_mul_ground`. These helpers returned
`[cf * c for cf in f]` and never stripped the result. They assumed that a nonzero
coefficient times a nonzero constant can never be zero. That is false in the `EX` domain:
`EX.__mul__` simplifies (`cancel().expand()`), so a coefficient that wasn't recognised as zero
can become `EX(0)` after multiplication. In the issue's case the result was `DMP([EX(0)], EX)`
instead of `DMP([], EX)`. It printed as `Poly(0, x, domain='EX')`, but `is_zero` returned
`False` and `terms_gcd()` raised `IndexError` (in older versions, `primitive()` raised
`ZeroDivisionError`, see #17990).

## Change

- `sympy/polys/densearith.py`: `dup_mul_ground` now returns `dup_strip(...)` of the product,
  and `dmp_mul_ground` returns `dmp_strip(..., u)`. This strips the result at every level of a
  multivariate polynomial. For ZZ/QQ and other domains without zero divisors, stripping does
  nothing and costs only a check of the leading coefficient.

## Verification

- New `test_issue_20427` in `sympy/polys/tests/test_polytools.py` uses the issue's example. It
  checks that `clear_denoms()` returns the canonical zero `Poly` (`rep == DMP([], EX)`), that
  `is_zero` is True, that `terms_gcd()` returns `((0,), Poly(0, x, domain='EX'))`, and that
  `primitive()` returns `(0, Poly(0, x, domain='EX'))`.
- Extended `test_dmp_mul_ground` in `sympy/polys/tests/test_densearith.py` with EX
  coefficients that vanish only after multiplication, in both the univariate and multivariate
  (inner-level) cases.
- Both tests fail without the change and pass with it.
- `bin/test sympy/polys sympy/simplify/tests/test_simplify.py sympy/solvers/tests/test_polysys.py`:
  998 passed, 6 skipped, 4 expected failures. The one XPASS (`test_apart_extension_xfail`) also
  happens without this change. Doctests for `densearith.py` and `densetools.py` pass.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
