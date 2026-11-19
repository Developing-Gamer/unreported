Escape DEL (0x7f) in parametrize test IDs

Root cause: the non-printable translate table in `_pytest/compat.py` excluded `range(32, 128)`, so 0x7f (DEL, non-printable) was left raw in str/bytes IDs, giving an invisible character.

Change: use `range(32, 127)`, so DEL becomes `\x7f`. Changelog fragment added.

Verification: manually confirmed `ascii_escaped(b"\x7f") == "\\x7f"`, and extended `test_idmaker_non_printable_characters` in testing/python/metafunc.py. That file could not be run here because `hypothesis` is not installed; testing/test_compat.py passes.
