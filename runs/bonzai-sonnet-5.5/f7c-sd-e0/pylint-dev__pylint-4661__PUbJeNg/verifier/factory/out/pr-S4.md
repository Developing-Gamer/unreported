Report unexpected messages in functional test mismatch summary

## Overview
When a functional test produced extra warnings, the failure summary said the results were wrong but only listed missing messages. The extra ones appeared only in the verbose "Actual pylint output" block. `LintModuleTest.multiset_difference` now returns both missing and unexpected messages, so the "Unexpected in testdata" section is shown.

## Details
`multiset_difference` computed `expected - actual` on `Counter`s. Counter subtraction discards zero and negative counts, so the loop that was meant to move negative counts into `unexpected` never found any, and `unexpected` was always empty. It now computes `missing = expected - actual` and `unexpected = actual - expected`.

Tests: `tests/testutils/test_lint_module_test.py` covers `multiset_difference` and `error_msg_for_unequal_messages` for the extra-message case (the "Unexpected" section appears, the "Expected" section does not) and the missing-message case.

## Verification
- New tests: 2 of 3 fail before the change (the `multiset_difference` and unexpected-section tests) and all pass after.
- `tests/testutils` and `tests/test_functional.py`: 515 passed, 20 skipped, 1 failed. The failure is `recursion_error_3152`, which also fails on the base commit (an extra `abstract-method` at line 6 in this environment). With this change its summary now lists it under "Unexpected in testdata", whereas before it listed nothing.
