Fix laguerre_poly silently ignoring an invalid alpha

## Overview
`laguerre_poly(n, x, alpha=<malformed>)` swallowed `TypeError`/`ValueError` from `construct_domain` (`SympifyError` is a `ValueError`) and fell back to `alpha=0`, so a bad shape parameter returned the same coefficients as omitting it. The error now propagates, as it already does in `jacobi_poly` and `gegenbauer_poly`. Only `alpha=None` defaults to 0.

## Details
- `sympy/polys/orthopolys.py`: removed the try/except around `construct_domain(alpha, field=True)`.
- `sympy/polys/tests/test_orthopolys.py`: `laguerre_poly(2, x, alpha=object())` must raise `ValueError`.

## Verification
- Before: new test fails with "DID NOT RAISE".
- After: `python -m pytest sympy/polys/tests/test_orthopolys.py` -> 7 passed; `laguerre_poly(2, x, alpha=S(1)/2)` still gives `x**2/2 - 5*x/2 + 15/8`.
