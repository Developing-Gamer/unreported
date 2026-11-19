Fix LintModuleTest.multiset_difference dropping unexpected messages

## Problem
When a functional test's expected and actual messages differ, the failure summary only listed messages that were missing. Extra (unexpected) messages never appeared in the "Unexpected in testdata" section; they were only visible in the verbose raw output.

## Cause
`multiset_difference` computed `expected - actual` on `Counter`s. The `-` operator discards zero and negative counts, so the loop that collects negative counts into `unexpected` could never fire.

## Fix
Use `missing = expected.copy(); missing.subtract(actual)`, which keeps negative counts, so the existing loop fills `unexpected` correctly. ChangeLog entry added.

## Verification
- New `tests/testutils/test_multiset_difference.py`: 2 of 3 tests fail on the base commit (`unexpected == {}`), all 3 pass after the fix.
- `pytest tests/test_functional.py`: `recursion_error_3152` fails both before and after (pre-existing). After the fix its message now includes `Unexpected in testdata: 6: abstract-method`, which was previously hidden.
