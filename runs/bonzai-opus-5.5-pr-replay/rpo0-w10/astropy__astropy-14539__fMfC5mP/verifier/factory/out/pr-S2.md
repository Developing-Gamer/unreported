Fix FITSDiff failing on variable-length array columns in the 'Q' format

## Overview
`FITSDiff` raised `ValueError: The truth value of an array with more than one element is ambiguous` when a table had a variable-length array column using the 64-bit `Q` descriptor (e.g. `QD`), even when a file was compared with itself. Such columns are now compared row by row, as `P` columns already were.

## Evidence
GitHub issue: "`io.fits.FITSDiff` may sometimes report differences between identical files". Reproduction: `Column('a', format='QD', array=[[0], [0, 0]])` written to a BinTableHDU, then `FITSDiff(f, f)`.

## Details
`TableDataDiff._diff` only used the per-row `np.allclose` comparison when `"P" in col.format`. `Q` columns fell through to `np.where(arra != arrb)` on an object array of ndarrays, which is ambiguous. The condition is now `"P" in col.format or "Q" in col.format`.

Tests added in `astropy/io/fits/tests/test_diff.py`: identical-file comparison for `PD` and `QD`, and a `QD` pair differing in one element (reports one differing row). Changelog: `docs/changes/io.fits/14539.bugfix.rst` (the number is a placeholder to be replaced by the real PR number).

## Verification
- Before the fix: `pytest astropy/io/fits/tests/test_diff.py -k vla` fails with the ValueError (2 failed, 1 passed).
- After: whole `test_diff.py` passes (51 passed); the issue snippet prints `True` for `identical`.
