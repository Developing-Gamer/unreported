Fix caplog.get_records() going stale after caplog.clear()

Root cause: `LogCaptureHandler.reset()` rebinds `self.records` to a new list. `caplog.clear()` used it, but the list for the current phase had already been stored in the item stash (used by `caplog.get_records()`), so the two diverged and `get_records()` was frozen after `clear()`.

Change: add `LogCaptureHandler.clear()` which clears the records list in place and resets the stream; `caplog.clear()` now uses it. `reset()` is unchanged for per-phase setup. Changelog fragment added.

Verification: new regression test `test_get_records_after_clear` in testing/logging/test_fixture.py; testing/logging passes.
