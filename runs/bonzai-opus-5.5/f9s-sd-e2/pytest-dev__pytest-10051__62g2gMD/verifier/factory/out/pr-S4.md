Escape the DEL byte (0x7f) in bytes-valued test IDs

## Problem
Test IDs built from `bytes` parametrize values containing `b"\x7f"` carried a raw, invisible DEL character instead of the escape text `\x7f`, making IDs unreliable to copy into rerun commands.

## Cause
`_non_printable_ascii_translate_table` in `src/_pytest/compat.py` excluded `range(32, 128)` from escaping, so DEL (127) was never escaped. `str` values were unaffected (`unicode_escape` already escapes DEL), but `bytes` values go through `decode("ascii", "backslashreplace")`, which leaves ASCII DEL untouched.

## Fix
Use `range(32, 127)` so DEL is escaped as `\x7f`. Added `test_ascii_escaped_bytes_del` in `testing/test_compat.py`.

## Verification
- `python -m pytest testing/test_compat.py -k ascii_escaped` failed before (`ab` with raw DEL vs `a\x7fb`), passes after.
- `--collect-only` on `parametrize("v", [b"a\x7fb"])` prints `test_v[a\x7fb]` with no raw DEL.
- `testing/python/metafunc.py` could not run here (missing `hypothesis`).
