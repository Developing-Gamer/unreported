Fix chained-comparison (R1716) false positive when a variable and a constant share the same text

## Overview
For `x < 'a' and a < y`, pylint suggested chaining the comparisons (R1716). The two comparisons are unrelated, and the suggested rewrite gives a different result. The checker now treats variable names and constants as different operands.

## Cause
`_check_chained_comparison` kept operand usage in one dict keyed by `operand.name` for `Name` nodes and `operand.value` for `Const` nodes. The variable `a` and the literal `'a'` therefore shared an entry and looked like a chain.

## Fix
Key the dict by `("name", name)` or `("const", value)`.

## Verification
- Added `test_not_simplify_chained_comparison_name_and_const` to `tests/functional/s/simplifiable/simplify_chained_comparison.py`. It failed before the fix and passes now.
- `python -m pytest tests/test_functional.py -k "chained or simplif"` passes, including the existing true-chain cases.
