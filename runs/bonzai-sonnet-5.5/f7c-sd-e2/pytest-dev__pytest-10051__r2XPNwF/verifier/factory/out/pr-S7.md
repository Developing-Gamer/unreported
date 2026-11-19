Fix caplog.get_records() going stale after caplog.clear()

## Overview
After `caplog.clear()`, `caplog.get_records(when)` stopped matching `caplog.records`: it kept the old records and never saw new ones. `clear()` now empties the records list in place, so both views stay in sync.

## Cause
At the start of each phase, `_runtest_for` stores `caplog_handler.records` in `item.stash[caplog_records_key][when]`. `caplog.clear()` called `LogCaptureHandler.reset()`, which rebinds `self.records = []`. `caplog.records` followed the new list, but the stashed list was orphaned.

## Changes
- Add `LogCaptureHandler.clear()`, which runs `self.records.clear()` and replaces the stream.
- `LogCaptureFixture.clear()` calls it instead of `reset()`.
- `reset()` is unchanged. It is still used at the start of each phase and needs to create a fresh list, so earlier phases' stored lists are not wiped.
- Add a changelog entry (`changelog/10003.bugfix.rst`; the number is a placeholder, since no issue number was available).

## Verification
- New test `testing/logging/test_fixture.py::test_clear_for_call_stage` failed before the fix (`get_records("call")` still held the pre-clear record) and passes now. It also checks that setup-phase records survive a call-phase clear.
- `PYTHONPATH=src python -m pytest testing/logging`: 60 passed.
