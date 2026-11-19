Fix tab completion adding a trailing `*` to prefixes that already contain a wildcard

## Overview
Tab completion with a wildcard filename pattern such as `test_*.py` also offered `test_a.py.bak`. `FastFilesCompleter` is meant to append `*` only when the prefix has no wildcard, but the check used `or` instead of `and`, so it was true unless both `*` and `?` were present. Wildcard patterns now complete to exactly the files they match; plain prefixes still complete as before.

## Details
- `src/_pytest/_argcomplete.py`: `if "*" not in prefix or "?" not in prefix` -> `if "*" not in prefix and "?" not in prefix`.
- `testing/test_argcomplete.py`: new `test_wildcard_prefix_not_extended` with `test_a.py`, `test_a.py.bak` and `test_b.py`. `test_*.py` and `test_?.py` return only the `.py` files, and the plain prefix `test_a` still returns both `test_a.py` and `test_a.py.bak`.

## Verification
- `python -m pytest testing/test_argcomplete.py -k wildcard --assert=plain`: fails before the fix (`test_*.py` also returns `test_a.py.bak`) and passes after.
- `python -m pytest testing/test_argcomplete.py testing/test_parseopt.py --assert=plain`: 31 passed, 1 skipped (argcomplete not installed).
- `--assert=plain` is needed only because assertion rewriting in this old pytest fails on Python 3.11 in this environment.
