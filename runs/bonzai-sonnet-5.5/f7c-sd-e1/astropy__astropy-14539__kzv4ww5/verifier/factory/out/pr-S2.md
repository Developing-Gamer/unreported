Fix FITSDiff/TableDataDiff on 64-bit variable-length array (Q) columns

## Overview
`FITSDiff` could report differences (or raise `ValueError: The truth value of an array with more than one element is ambiguous`) when comparing a file to itself if it had a 64-bit variable-length array column such as `QD`. `TableDataDiff` only used its row-by-row variable-length comparison for `P` formats; `Q` columns fell through to `np.where(arra != arrb)` on an object array of ndarrays. Q columns now take the per-row path, and rows of different length are reported as different (previously a length-1 row could broadcast against a longer one and compare equal).

## Details
- `astropy/io/fits/diff.py`: `TableDataDiff._diff` treats `"P"` or `"Q"` formats as VLA; rows whose shapes differ count as differing.
- Tests in `astropy/io/fits/tests/test_diff.py`: identical-file check for `PD` and `QD` (the issue's reproduction), and a differing-rows check (value and length).
- Changelog: `docs/changes/io.fits/14539.bugfix.rst` (the number is a placeholder guess; rename to the real PR number).

## Verification
- Before the fix the new tests fail (3 of 4; QD raises the ambiguous-truth-value ValueError).
- After: `pytest astropy/io/fits/tests/test_diff.py astropy/io/fits/tests/test_table.py` -> 165 passed, 3 skipped.
