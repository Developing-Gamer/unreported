Label `--pastebin=failed` links with the crash location, not the outermost traceback entry

## Overview
With `--pastebin=failed`, each paste URL is printed after a label taken from the traceback. The label used the first traceback entry, which for a failure raised inside a helper is the test's call to the helper (`test_h.py:5:`). The pasted traceback ends at the assertion in the helper (`test_h.py:2: AssertionError`), so the label and the paste disagreed. The label now uses the last entry, where the error was raised.

## Details
- `src/_pytest/pastebin.py`: `reprentries[0]` -> `reprentries[-1]` in `pytest_terminal_summary`.
- `testing/test_pastebin.py`: new `test_failed_helper_label_uses_crash_location` (test calls a helper that asserts; paste upload stubbed; expects `test_h.py:2: AssertionError --> http://paste/1`).
- `changelog/5822.bugfix.rst`: changelog entry. The number 5822 is a placeholder; rename it to the real issue/PR number.

## Verification
- Before the fix: `python -m pytest testing/test_pastebin.py -q --assert=plain -p no:cacheprovider -k helper` fails, output `test_h.py:5: --> http://paste/1`.
- After the fix: the same command passes (1 passed).
- The new test passes `--assert=plain` to the inner run only because this environment's pytest cannot rewrite asserts on Python 3.11; the other pastebin tests (`test_failed`, `test_all`, `test_non_ascii_paste_text`) fail here on that same pre-existing issue.
