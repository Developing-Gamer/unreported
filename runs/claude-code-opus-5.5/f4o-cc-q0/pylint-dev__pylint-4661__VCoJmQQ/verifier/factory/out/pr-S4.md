Report unexpected messages in functional test mismatch summary

## Root cause
`LintModuleTest.multiset_difference` computed `missing = expected_entries - actual_entries`. `Counter.__sub__` drops every count that is zero or negative, so the following loop that collects negative counts into `unexpected` never ran. When a functional test failed because pylint emitted extra messages, the "Wrong results" summary had no "Unexpected in testdata" section. The extra messages only showed up in the verbose actual-output dump.

## Change
Copy the expected counter and use `Counter.subtract`, which keeps negative counts, so the existing loop splits the result into missing and unexpected entries.

## Verification
- New `tests/testutils/test_lint_module_output_update.py` checks a mix of missing and unexpected entries, and a case with only unexpected entries. Both tests fail before the fix and pass after it.
- After the fix, a failing functional test prints "Unexpected in testdata: 228: unused-private-member" as expected (this came up while developing the S1 test).
- `pytest tests/test_functional.py tests/testutils`: everything passes except the pre-existing `recursion_error_3152` failure, which is caused by the astroid version installed in this environment.
