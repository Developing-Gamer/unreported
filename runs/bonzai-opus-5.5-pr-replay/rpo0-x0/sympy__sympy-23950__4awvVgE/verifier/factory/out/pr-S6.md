Implement Contains.as_set for a Symbol element

`Contains(x, Reals).as_set()` used to give no set (originally returned the `Contains` itself, now a bare `NotImplementedError`). Because of that, anything converting a condition to a set failed: `Piecewise((6, Contains(x, Reals)), (7, True))`, `And(Contains(...), ...).as_set()`, etc.

For a Symbol `x`, `Contains(x, S)` holds exactly when `x` is in `S`, so `as_set()` now returns `S`. For a non-Symbol element it still raises `NotImplementedError` (with a message), since the set of the free variable is not simply `S`.

Tests: updated `test_as_set` in `sympy/sets/tests/test_contains.py` (fails before the fix with NotImplementedError); added And and Piecewise.as_expr_set_pairs cases. Added a doctest.

Verification: `python -m pytest sympy/sets/tests/test_contains.py sympy/functions/elementary/tests/test_piecewise.py sympy/logic/tests/test_boolalg.py` -> 150 passed, 1 xfailed; `bin/doctest sympy/sets/contains.py` passes.
