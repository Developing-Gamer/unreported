Fix caplog.get_records() going stale after caplog.clear()

## Problem
After `caplog.clear()`, `caplog.get_records("call")` kept the old records and never saw new ones, while `caplog.records` behaved correctly.

## Cause
`_runtest_for` stores the handler's `records` list in the item stash for `get_records()`. `caplog.clear()` called `LogCaptureHandler.reset()`, which rebinds `self.records` to a new list, so the stash kept pointing at the old, now-orphaned list.

## Fix
Add `LogCaptureHandler.clear()`, which empties the existing list in place and replaces the stream. `LogCaptureFixture.clear()` uses it. `reset()` is unchanged, so the per-phase reset still leaves earlier phases' lists (e.g. setup records) intact.

## Verification
- New test `testing/logging/test_fixture.py::test_clear_keeps_get_records_in_sync`: fails before (`assert [<LogRecord ...>] == []`), passes after.
- `pytest testing/logging` : 60 passed.
