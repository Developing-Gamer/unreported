Implement Contains.as_set so it returns the set instead of raising NotImplementedError

## Overview
`Contains(x, S).as_set()` raised `NotImplementedError` (sympy/sets/contains.py:48; 723 Sentry events, 109 users in 7 days) even for valid input. `Contains(x, S)` says "x is in S", so its solution set in `x` is `S`; it now returns `S`.

## Details
- `Contains.as_set` returns `self.args[1]` when the element is a `Symbol`. For a non-symbol element (e.g. `x + 1`) the solution set is not simply `S`, so it still raises `NotImplementedError` with an explanatory message rather than returning a wrong answer.
- Added a doctest, and updated `test_as_set` in sympy/sets/tests/test_contains.py (which previously asserted the NotImplementedError).

## Proof
Before (base commit): `python bin/test sympy/sets/tests/test_contains.py` fails in `test_as_set` with `NotImplementedError` at contains.py line 48. After: passes.

## Verification
- `python bin/test sympy/sets/tests/test_contains.py`
- `python bin/test sympy/sets sympy/logic sympy/functions/elementary/tests/test_piecewise.py`: 379 passed, 0 failures (one unrelated pre-existing xpass in test_powerset).
- `python bin/doctest sympy/sets/contains.py`: passed.
