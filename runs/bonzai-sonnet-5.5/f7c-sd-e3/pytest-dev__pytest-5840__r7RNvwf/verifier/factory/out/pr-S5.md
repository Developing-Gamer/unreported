Fix argcomplete FastFilesCompleter appending '*' to prefixes that already contain a wildcard

## Overview
Tab completion with a pattern such as `test_*.py` also offered `test_a.py.bak`. `FastFilesCompleter` appended a trailing `*` whenever the prefix lacked either `*` or `?` (`or`), so `test_*.py` became `test_*.py*`. It now appends `*` only when the prefix has neither wildcard. Plain prefixes such as `test_` complete as before.

## Evidence
CLI support channel: "Tab completion sometimes offers .py.bak files when my test filename pattern ends in .py. Completing ordinary filenames still looks normal."

## Details
- `src/_pytest/_argcomplete.py`: `"*" not in prefix or "?" not in prefix` -> `and`.
- `testing/test_argcomplete.py`: new `test_wildcard_prefix_not_extended` (`test_*.py` and `test_a.p?` return only `test_a.py`; `test_` still returns both files).
- `changelog/5813.bugfix.rst` (number is a placeholder; rename to the real issue/PR number).

## Verification
- Before the fix: `python -m pytest testing/test_argcomplete.py -q` fails with `AssertionError: assert ['test_a.py', 'test_a.py.bak'] == ['test_a.py']`.
- After the fix: the same command passes (3 passed).
