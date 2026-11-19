Don't treat `pytest_report_header` as a firstresult hook

Root cause: `pytest_report_header` in `src/_pytest/hookspec.py` was decorated with `@hookspec(firstresult=True)`. Pluggy therefore stopped at the first implementation returning a non-None value, so with several plugins/conftests only one contributed to the session header (e.g. the runtime label was shown, but the build metadata from another implementation vanished). The terminal reporter already merges and flattens lists of lines from all implementations.

Change: removed the `firstresult=True` marker so all implementations are called and their lines are all displayed.

Verification: added `test_pytest_report_header_multiple_plugins` in testing/test_terminal.py (fails before, passes after); the existing `test_pytest_report_header` tests, which expect lines from multiple conftests, also pass now. Added changelog/6240.bugfix.rst.
