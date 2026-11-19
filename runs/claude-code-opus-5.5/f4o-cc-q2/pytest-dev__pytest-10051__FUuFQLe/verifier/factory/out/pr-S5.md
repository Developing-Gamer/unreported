Honour fractional faulthandler_timeout values

**Root cause**
`_pytest.faulthandler.get_timeout_config_value` returned `int(float(config.getini("faulthandler_timeout") or 0.0))`. The `int()` truncates any timeout below one second to `0`, and `pytest_runtest_protocol` treats `0` as "disabled". So `faulthandler_timeout = 0.5` silently stopped producing thread dumps for hanging tests, while `5` kept working. The value also gets truncated for other values, e.g. `1.5` became `1`.

**Change**
- `src/_pytest/faulthandler.py`: return `float(...)` without the `int()` truncation. `faulthandler.dump_traceback_later` accepts float timeouts.

**Verification**
- I added `test_timeout_config_value_keeps_fraction`, parametrized over `0.5`, `0.01`, `5` and `1.5`, to `testing/test_faulthandler.py`. Before the change, the `0.5`, `0.01` and `1.5` cases fail. After the change, all cases pass.
- The existing `test_timeout` already uses `faulthandler_timeout = 0.01`. All of `testing/test_faulthandler.py` passes.

(No towncrier changelog entry was added because no upstream issue number is known. Add `changelog/<issue>.bugfix.rst` when filing.)
