Escape DEL (0x7f) in auto-generated parametrize ids

**Root cause**
`_pytest.compat._non_printable_ascii_translate_table` was built with `range(32, 128)` as the "printable" range. That range includes 127 (DEL), which is a control character. So `ascii_escaped(b"\x7f")` returned a raw invisible DEL instead of the text `\x7f`. Test IDs for bytes parameters that contain 0x7f therefore had an invisible character, and copying them into rerun commands (`pytest "test_x[...]"`) did not work reliably.

**Change**
- `src/_pytest/compat.py`: the printable range is now `range(32, 127)`, so 0x7f is escaped like every other non-printable ASCII byte.

**Verification**
- I added `b"\x7f"` and `b"a\x7fb"` cases to `TestMetafunc.test_bytes_idval` in `testing/python/metafunc.py`. They fail before the change and pass after it.
- I ran `testing/python/metafunc.py`, `testing/python/collect.py` and `testing/test_compat.py`: all pass.

(No towncrier changelog entry was added because no upstream issue number is known. Add `changelog/<issue>.bugfix.rst` when filing.)
