Stop laguerre_poly from silently replacing a malformed alpha with 0

## Overview
`laguerre_poly(n, x, alpha)` wrapped `construct_domain(alpha)` in `try/except (TypeError, ValueError)` and fell back to `alpha = 0`. A malformed shape parameter therefore produced the plain Laguerre polynomial, with coefficients identical to leaving `alpha` blank, instead of failing validation. `jacobi_poly` and `gegenbauer_poly` do not guard this call and raise.

## Details
- Removed the swallowing `try/except` in `sympy/polys/orthopolys.py`; the `alpha is None` branch still uses `QQ(0)`.
- `construct_domain` accepts sequences/dicts, which would later fail with an obscure `TypeError`; `laguerre_poly` now raises a clear `ValueError` ("alpha must be a single number or expression") for those.
- Regression test in `test_laguerre_poly`: malformed alpha (`[1, 2]`, `'zz'`) raises `ValueError`.

## Verification
`python bin/test sympy/polys/tests/test_orthopolys.py`: the new test fails on the base commit (TypeError raised from `dup_laguerre`, not ValueError) and all 7 tests pass after the change. Valid numeric/symbolic alpha results are unchanged (existing assertions pass).
