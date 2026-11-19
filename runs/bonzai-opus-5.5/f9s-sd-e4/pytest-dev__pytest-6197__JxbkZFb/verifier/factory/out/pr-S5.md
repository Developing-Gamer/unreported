Restore conftest.py/plugin lines in the terminal header (pytest_report_header is not firstresult)

## Overview
The test-run banner printed the platform/Python line but dropped build metadata that `conftest.py` files and plugins add through `pytest_report_header`. The hook spec was declared `@hookspec(firstresult=True)`, so pluggy stopped at the first non-`None` result (the terminal reporter's own rootdir/plugins lines) and never called the others. Removing `firstresult` makes every implementation's lines show again, which is what `TerminalReporter.pytest_sessionstart` already expects (it reverses and flattens a list of results).

## Evidence
Support channel report: "The test-run banner still shows our runtime label, but the build metadata has disappeared. The tests themselves finish normally."

## Details
- `src/_pytest/hookspec.py`: remove `firstresult=True` from `pytest_report_header`.
- `changelog/6214.bugfix.rst`: changelog entry.
- No new test: the existing `testing/test_terminal.py::TestGenericReporting::test_pytest_report_header` covers it (conftest and subdirectory conftest header lines). It failed on the base commit in 4 variants and passes now.

## Verification
- `python -m pytest testing/test_terminal.py -k header`: base 4 failed / 3 passed; with fix 7 passed.
- `testing/test_terminal.py testing/test_helpconfig.py testing/test_cacheprovider.py`: 182 passed; the one failure, `test_cache_failure_warns`, fails identically on the base commit (the tests run as root, so the cache dir is writable).
- The `test_cache_reportheader*` tests in test_cacheprovider.py also failed on base and pass now.
