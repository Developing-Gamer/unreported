Show `pytest_report_header` lines from all plugins (drop erroneous `firstresult`)

## Root cause
The `pytest_report_header` hookspec in `src/_pytest/hookspec.py` was declared with `@hookspec(firstresult=True)`. The hook is documented to return "a string or list of strings" from each plugin, and `TerminalReporter.pytest_sessionstart` collapses the list of results from all implementations. With `firstresult`, pluggy stops at the first non-None result, so only one implementation's lines appear in the session banner. Header lines from conftests/other plugins (e.g. build metadata) disappear while the run itself works normally.

## Change
- Removed `firstresult=True` from the `pytest_report_header` hookspec.

## Verification
- Manual: a conftest returning `["runtime: r1", "build: b42"]` produced no header lines before the change. After it, both lines are shown, followed by pytest's own `rootdir:` line.
- The existing `testing/test_terminal.py::TestGenericReporting::test_pytest_report_header[*]` (4 params) failed before and passes now.
- New `test_pytest_report_header_all_plugins` checks that conftest lines and pytest's `rootdir:` line both appear. It fails before the change and passes after it.
- `testing/test_terminal.py` passes in full.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
