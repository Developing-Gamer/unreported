Fix faulthandler_timeout truncating sub-second values to 0

Hanging tests produced no thread dump with `faulthandler_timeout = 0.5`, while whole-second values such as 5 still worked.

## Cause
`get_timeout_config_value` in `src/_pytest/faulthandler.py` returned `int(float(...))`, so 0.5 became 0 and the `timeout > 0` check in `pytest_runtest_protocol` skipped `faulthandler.dump_traceback_later`. Values like 5.5 were silently cut to 5.

## Fix
Return `float(...)`, which matches the annotation and what `dump_traceback_later` accepts.

## Tests
Added `test_timeout_subsecond_is_not_truncated` in `testing/test_faulthandler.py`. It sets `faulthandler_timeout = 0.5` and asserts the config value is 0.5 and that `dump_traceback_later` is called with 0.5. It failed before the fix (`assert 0 == 0.5`) and passes after. Added changelog/10002.bugfix.rst.
