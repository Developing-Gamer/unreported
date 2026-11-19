Fix import of astropy.io.ascii when docstrings are stripped (python -OO)

## Overview
`import astropy.io.ascii` (and so `astropy.table`) crashed under `python -OO` with `AttributeError: 'NoneType' object has no attribute 'expandtabs'`. `MetaBaseReader.__init__` appended `inspect.cleandoc(cls.__doc__)` to the generated reader/writer docstrings without checking for `None`; with `-OO` every class docstring is `None`. The class docstring is now appended only when it exists.

## Details
- `astropy/io/ascii/core.py`: guard both `cleandoc(cls.__doc__)` calls (reader and writer registry docstrings). Behaviour is unchanged when docstrings exist.
- `astropy/io/ascii/tests/test_read.py`: `test_import_with_stripped_docstrings` runs `python -OO -c "import astropy.io.ascii, astropy.table"` in a subprocess (skipped if already running with -OO).
- `docs/changes/io.ascii/14000.bugfix.rst`: changelog (number is a placeholder; rename to the PR number).

## Verification
- Before: the new test fails with `AttributeError: 'NoneType' object has no attribute 'expandtabs'`.
- After: it passes; `pytest astropy/io/ascii/tests` -> 826 passed, 36 skipped, 6 xfailed.
