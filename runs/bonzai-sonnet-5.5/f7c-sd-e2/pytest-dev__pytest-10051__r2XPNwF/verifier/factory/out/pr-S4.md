Escape DEL (0x7f) in bytes parametrize IDs

Bytes parameters containing `0x7f` (DEL) got a raw, invisible DEL character in their test ID instead of the `\x7f` escape text, so IDs copied from reports into rerun commands were unreliable.

## Cause
`_non_printable_ascii_translate_table` in `src/_pytest/compat.py` was built with `range(32, 128)` as the "printable" set, which wrongly includes 127 (DEL). It is now `range(32, 127)`. (`str` values already went through `unicode_escape`, which escapes DEL.)

## Proof
Before: `PYTHONPATH=src python -m pytest testing/python/metafunc.py -k non_printable -q -p no:cacheprovider` fails with `At index 7 diff: '\x7f-8' != '\\x7f-8'`.
After: the same command passes.

## Verification
`testing/python/metafunc.py` and `testing/test_compat.py`: 114 passed, 1 skipped. Extended `test_idmaker_non_printable_characters` with str and bytes DEL cases; added a changelog entry (the number 10001 is a placeholder, rename it to the issue/PR number).
