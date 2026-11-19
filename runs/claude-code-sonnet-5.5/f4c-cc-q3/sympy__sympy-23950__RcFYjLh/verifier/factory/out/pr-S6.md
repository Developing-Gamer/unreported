Make Contains.as_set return the underlying Set instead of raising

Root cause: `Contains.as_set()` raised `NotImplementedError`. Boolean `as_set()` is meant to return the set of values for which the condition holds, and the one-variable `Contains(x, S)` holds exactly when `x` is in `S`. Callers that rely on `cond.as_set().as_relational(x)`, such as Piecewise condition handling, therefore failed. This also accounts for the production Sentry `NotImplementedError` at `sympy/sets/contains.py` `as_set` (S7).

Change: `Contains.as_set` returns `self.args[1]`. The test that expected `NotImplementedError` is replaced with tests asserting the returned Set and that `as_relational` works on it.

Verification: ran `bin/test` on `sympy/sets`, `sympy/logic` and `sympy/functions/elementary/tests/test_piecewise.py`. All pass.

Also covers S7 (same root cause).
