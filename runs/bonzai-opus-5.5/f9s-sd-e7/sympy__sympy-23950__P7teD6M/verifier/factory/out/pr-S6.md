Fix Contains.as_set so a symbol-membership condition becomes its set

## Overview
`Contains(x, Reals).as_set()` used to return the `Contains` itself (a boolean, not a set) and now raised `NotImplementedError`. Callers that turn conditions into sets, such as `Piecewise((6, Contains(x, Reals)), (7, True))`, `And(...).as_set()` and `Piecewise.as_expr_set_pairs`, therefore failed. `as_set` now returns the set the symbol is in.

## Details
- `sympy/sets/contains.py`: `Contains.as_set` returns `self.args[1]` when the element is a `Symbol`. For any other element (e.g. `x + 1`) the set of `x` is not simply the set, so it still raises `NotImplementedError` with a clear message.
- `sympy/sets/tests/test_contains.py`: `test_as_set` now asserts `Contains(x, FiniteSet(y)).as_set() == FiniteSet(y)`, `Contains(x, Reals).as_set() == Reals`, `And(Contains(x, Interval(0, 2)), x > 1).as_set() == Interval.Lopen(1, 2)`, the `Piecewise` `as_expr_set_pairs` case, and the non-symbol error.

## Verification
- Before: `python -m pytest sympy/sets/tests/test_contains.py` fails `test_as_set` with `NotImplementedError`.
- After: that file passes, as do `sympy/sets`, `sympy/functions/elementary/tests/test_piecewise.py`, `sympy/logic` and the doctest of `contains.py`.
