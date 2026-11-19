Fix unneeded-not suggesting a non-equivalent comparison when the right operand is a set

## Overview
`not a <= b` is not equivalent to `a > b` for sets, so `unneeded-not` skips comparisons involving sets. The guard only inspected the left operand, so `not {}.keys() <= set(x)` or `not KEYS <= GROUP` (set on the right) still got the suggestion `KEYS > GROUP`. For disjoint groups the original expression is `True` and the suggested one is `False`.

## Details
- `NotChecker.visit_unaryop` now applies the set/frozenset/uninferable guard to both operands.
- Added tolerated cases to `tests/functional/u/unnecessary/unnecessary_not.py` (set on the right, keys view vs. set/frozenset/literal set); the test file also disables `misplaced-comparison-constant` for the `3 <= set(...)` case. ChangeLog entry added.
- Before the fix the functional test failed with "Unexpected in testdata: unneeded-not" on the new lines.

## Verification
`python -m pytest tests/test_functional.py -k 'unnecessary_not or consider_using_in or superfluous_parens'`: 3 passed.
