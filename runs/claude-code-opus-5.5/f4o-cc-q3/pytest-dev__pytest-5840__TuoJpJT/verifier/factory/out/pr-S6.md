pastebin: label failed-test paste links with the failing line's location

## Root cause
With `--pastebin=failed`, `pytest_terminal_summary` labeled each paste URL with `rep.longrepr.reprtraceback.reprentries[0].reprfileloc`. That is the outermost traceback entry, i.e. the call inside the test function. When the assertion fails inside a helper, the label pointed at the test's call to the helper, not at the failing line shown in the pasted traceback.

## Change
`src/_pytest/pastebin.py` now uses `reprentries[-1]`, the innermost entry where the failure happened.

## Verification
- Added `TestPasteCapture::test_failed_label_uses_crash_location` in `testing/test_pastebin.py`. The assertion fails in a helper, and the test checks that the summary line reads `<file>:2: AssertionError --> URL`. It fails before the change and passes after.
- `testing/test_pastebin.py` passes.
