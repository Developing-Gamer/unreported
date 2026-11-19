Fix caplog.get_records() going out of sync after caplog.clear()

## Overview
`caplog.clear()` replaced the handler's `records` list with a new one, while `item.stash[caplog_records_key][when]` (what `caplog.get_records(when)` returns) kept pointing to the old list. After `clear()`, `get_records()` was frozen: never cleared and never given new records. `clear()` now empties the list in place, so both views stay identical.

## Evidence
GitHub issue "caplog.get_records and caplog.clear conflict".

Before (base commit), `PYTHONPATH=src python -m pytest testing/logging/test_fixture.py -k test_clear_for_call_stage`:
`assert [<LogRecord ... "a_call_log">] == []` (get_records("call") still holds the cleared record).
After: passes; `testing/logging` is 60 passed.

## Details
- Added `LogCaptureHandler.clear()` (`records.clear()` + new `StringIO`); `LogCaptureFixture.clear()` uses it.
- `reset()` is unchanged: `_runtest_for` calls it at the start of each phase and needs a fresh list per phase so earlier phases' stored records (e.g. setup) survive.
- Test `test_clear_for_call_stage` also checks setup records survive a clear in the call phase.
- Changelog: `changelog/9877.bugfix.rst`.

## Verification
`python -m pytest testing/logging` (60 passed).
