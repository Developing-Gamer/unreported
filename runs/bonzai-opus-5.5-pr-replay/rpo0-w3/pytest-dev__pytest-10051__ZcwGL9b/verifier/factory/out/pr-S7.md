Fix caplog.get_records() going stale after caplog.clear()

## Overview
`caplog.clear()` replaced the capture handler's `records` list with a new one, but `caplog.get_records(when)` still pointed at the old list. After `clear()`, `get_records()` kept the cleared records and never saw new ones, so it disagreed with `caplog.records`. `clear()` now empties the list in place, so both stay in sync.

## Evidence
GitHub issue: "caplog.get_records and caplog.clear conflict".

Before the fix, the new test fails with:
`assert [<LogRecord: ... "a_call_log">] == []` at `caplog.get_records("call") == []` after `caplog.clear()`.

## Details
- Added `LogCaptureHandler.clear()`, which calls `self.records.clear()` and resets the stream. The list object stays the same.
- `LogCaptureFixture.clear()` calls `handler.clear()` instead of `handler.reset()`.
- `reset()` is unchanged. It still rebinds, which is needed so the per-phase reset doesn't wipe the `setup` records stashed for `get_records("setup")`.
- Added `test_clear_for_call_stage`. It checks `get_records("call")` before and after `clear()` and after logging again, that setup records survive, and that `get_records("call") == caplog.records`.
- Added a changelog entry. The `9877` in its file name is a placeholder guess and must be renamed to the real issue number.

## Verification
`python -m pytest testing/logging -q` gives 60 passed. The new test fails on the base commit and passes with the fix.
