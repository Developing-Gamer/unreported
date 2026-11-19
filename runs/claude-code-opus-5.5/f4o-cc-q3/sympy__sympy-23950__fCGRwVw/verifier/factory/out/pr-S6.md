Make Contains.as_set() return the set instead of raising NotImplementedError

Fixes S6 (GitHub issue "Contains.as_set returns Contains") and S7 (production Sentry NotImplementedError at sympy/sets/contains.py in as_set, 723 events / 109 users in 7 days); both have the same root cause.

## Root cause
`Contains(x, S)` is a Boolean. `Boolean.as_set()` is supposed to return the set of values of its free symbol for which the condition is true. `Contains` overrode `as_set` with `raise NotImplementedError()`. Callers such as Piecewise condition handling and `as_set().as_relational(x)` chains then fail: either with the NotImplementedError from S7, or, in older versions, with `AttributeError: 'Contains' object has no attribute 'as_relational'` (S6).

## Change
- `sympy/sets/contains.py`: `Contains.as_set()` now returns `self.args[1]`, the set. This means `Contains(x, Reals).as_set() == Reals`, which is a real `Set` with `as_relational`.
- `sympy/sets/tests/test_contains.py`: `test_as_set` now checks the returned sets (FiniteSet, Integers, Reals) instead of expecting NotImplementedError. A new regression test builds `Piecewise((6, Contains(x, Reals)), (7, True))`.

## Verification
- On the old `contains.py`, the new `test_as_set` fails with NotImplementedError. With the fix it passes.
- `bin/test sympy/sets/tests/test_contains.py sympy/functions/elementary/tests/test_piecewise.py sympy/logic/tests/test_boolalg.py sympy/sets/tests/test_sets.py sympy/solvers/tests/test_inequalities.py`: 277 passed, 5 skipped, 8 expected failures, no failures.
