Keep fractional faulthandler_timeout values

Root cause: `get_timeout_config_value` wrapped the value in `int(float(...))`, truncating e.g. `0.5` to `0`, which disables `dump_traceback_later`. A 5 s timeout worked, 0.5 s did not.

Change: return `float(...)`; `faulthandler.dump_traceback_later` accepts floats. Changelog fragment added.

Verification: new test `test_timeout_config_value_keeps_fractions` in testing/test_faulthandler.py; the file passes.
