Fix AttributeError importing astropy.io.ascii under python -OO

## Overview
`from astropy.io import ascii` (and so every ASCII `Table.read/write`) crashed under `python -OO` with `AttributeError: 'NoneType' object has no attribute 'expandtabs'`. `-OO` strips docstrings, so `cls.__doc__` is `None` when the ASCII reader/writer classes are registered. Importing now works.

## Details
- `MetaBaseReader.__init__` in `astropy/io/ascii/core.py` appended `inspect.cleandoc(cls.__doc__)` to the generated read/write help text. It now uses `cls.__doc__ or ""`, so the per-format details section is simply empty when docstrings are stripped.
- Regression test `test_import_with_stripped_docstrings` (`astropy/io/ascii/tests/test_read.py`) runs `python -OO` in a subprocess, imports `astropy.io.ascii` and reads a CSV.
- Changelog: `docs/changes/io.ascii/14100.bugfix.rst`.
- Open PRs #1000 and #1001 touch rst.py / timeseries and do not address this.

## Verification
- Before: the new test fails with `AttributeError: 'NoneType' object has no attribute 'expandtabs'` (core.py:1234).
- After: it passes; `pytest astropy/io/ascii/tests` gives 827 passed, 36 skipped, 6 xfailed.
