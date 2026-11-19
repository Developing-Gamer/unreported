Keep caplog.get_records() in sync after caplog.clear()

**Root cause**
During each test phase, `LoggingPlugin._runtest_for` stores `caplog_handler.records` in `item.stash[caplog_records_key][when]`. `caplog.get_records(when)` returns that same list object. `LogCaptureFixture.clear()` called `LogCaptureHandler.reset()`, which *rebinds* `self.records = []`. After that, the handler appends new records to a new list, while `get_records()` still returns the old list. That old list is never cleared and never receives new records.

**Change**
- `src/_pytest/logging.py`: I added `LogCaptureHandler.clear()`, which empties the existing records list in place (`self.records.clear()`) and resets the stream. `LogCaptureFixture.clear()` now calls `handler.clear()` instead of `handler.reset()`. `reset()` keeps rebinding, as before, because the plugin uses it between phases so that each phase keeps its own list.
- `changelog/9877.bugfix.rst`: changelog entry.

**Verification**
- I added `test_clear_keeps_get_records_in_sync` to `testing/logging/test_fixture.py`, based on the issue's reproducer. It also checks that records logged after `clear()` show up in `get_records("call")`. It fails before the change and passes after it.
- All of `testing/logging/` passes.
