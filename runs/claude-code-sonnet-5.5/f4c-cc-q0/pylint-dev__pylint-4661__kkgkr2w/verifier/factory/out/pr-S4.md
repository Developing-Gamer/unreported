Report unexpected messages in functional test mismatch summary

Root cause: `LintModuleTest.multiset_difference` computed `missing = expected - actual` with `collections.Counter`, which discards non-positive counts, then looped looking for negative values to fill `unexpected`. That never happens, so `unexpected` was always empty and extra warnings were omitted from the "Wrong results" summary (only visible in verbose output).

Change: `unexpected = actual_entries - expected_entries` (pylint/testutils/lint_module_test.py); removed the now-unused `Dict` import. Fixing this also surfaced two real `unused-private-member` messages in a new functional test, confirming the summary works.

Verification: added `test_multiset_difference_reports_missing_and_unexpected` in tests/testutils/test_output_line.py (fails before, passes after).
