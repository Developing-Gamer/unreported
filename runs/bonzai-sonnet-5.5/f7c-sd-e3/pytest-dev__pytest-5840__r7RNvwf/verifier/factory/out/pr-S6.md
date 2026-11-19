Fix --pastebin=failed label pointing at the test's call line instead of the assertion

## Overview
With `--pastebin=failed`, the label printed next to each paste URL came from the first traceback entry, which is the outer test's call line. When the failure happens inside a helper, the label named the `helper()` call and not the assertion shown in the pasted traceback. The label now uses the last entry, where the failure happened.

## Evidence
CI triage chat: "For failures that go through a helper, the paste link is labeled with the outer test call's location rather than the assertion location shown in the pasted traceback."

Before: `test_helper_fail.py:5: --> None` (line 5 is the call to `helper()`).
After: `test_helper_fail.py:2: AssertionError --> ...` (line 2 is the assertion).

## Details
- `src/_pytest/pastebin.py`: `reprentries[0].reprfileloc` -> `reprentries[-1].reprfileloc`. The `AttributeError` fallback to the failure headline is kept for native tracebacks.
- `testing/test_pastebin.py`: new `test_failed_label_uses_assertion_location`; it fails on the base commit and passes with the fix.

## Verification
`python -m pytest testing/test_pastebin.py` -> 6 passed.
