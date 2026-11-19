Fix faulthandler_timeout truncating sub-second timeouts to 0

## Problem
With `faulthandler_timeout = 0.5`, hanging tests no longer produced thread dumps; a 5-second timeout still did.

## Cause
`get_timeout_config_value` in `src/_pytest/faulthandler.py` wrapped the value in `int()`, so `0.5` became `0`. `pytest_runtest_protocol` only arms `faulthandler.dump_traceback_later` when `timeout > 0`, so the dump was silently disabled. Fractional values above 1 (e.g. `2.5`) were also truncated.

## Fix
Return `float(config.getini("faulthandler_timeout") or 0.0)` without the `int()` truncation. Added `changelog/9751.bugfix.rst`.

## Verification
- New test `testing/test_faulthandler.py::test_timeout_config_value_is_not_truncated` (0.5, 2.5, 3): fails on base (`assert 2 == 2.5`, 0.5 -> 0), passes with the fix.
- Command: `PYTHONPATH=src python -m pytest testing/test_faulthandler.py -k config_value -q`
- Other tests in the file that spawn subprocesses (test_enabled, test_disabled, etc.) fail identically on base in this sandbox because the subprocess interpreter has no pytest installed; unrelated.
