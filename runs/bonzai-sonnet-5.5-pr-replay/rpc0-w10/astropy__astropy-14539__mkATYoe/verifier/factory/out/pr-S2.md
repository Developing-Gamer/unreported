Fix FITSDiff/TableDataDiff on 64-bit variable-length array (Q) columns

## Problem
`FITSDiff` could raise `ValueError: The truth value of an array with more than one element is ambiguous` (or report differences) when comparing a file with itself if it had a `Q`-format variable-length-array column, e.g. `Column('a', format='QD', array=[[0], [0, 0]])`.

## Cause
`TableDataDiff._diff` only used the per-row VLA comparison for columns with `"P"` in the format. `Q` columns fell through to `np.where(arra != arrb)` on an object array of ndarrays, which compares whole arrays elementwise-ambiguously.

## Fix
Use the per-row comparison for `P` and `Q` columns. Rows whose shapes differ are now counted as different (previously `np.allclose` would broadcast, e.g. `[0]` vs `[0, 0]`).

## Verification
- New tests `test_fitsdiff_vla_identical` / `test_fitsdiff_vla_different` (PD and QD): the QD cases failed before with the ValueError above and pass now.
- `pytest astropy/io/fits/tests/test_diff.py astropy/io/fits/tests/test_table.py`: 165 passed, 3 skipped.
- Changelog: docs/changes/io.fits/14539.bugfix.rst (number is a placeholder to match the PR number).
