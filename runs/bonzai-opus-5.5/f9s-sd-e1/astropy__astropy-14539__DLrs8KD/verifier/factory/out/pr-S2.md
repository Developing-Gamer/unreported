Fix FITSDiff failing on variable-length array columns in 'Q' format

## Problem
`FITSDiff` could raise `ValueError: The truth value of an array with more than one element is ambiguous` (or report differences) for tables with variable-length array (VLA) columns, even when a file is compared with itself. `TableDataDiff._diff` only used the per-row `np.allclose` comparison when `"P" in col.format`. VLA columns using the 64-bit `Q` descriptor (e.g. `QD`) fell through to `np.where(arra != arrb)` on an object array of per-row arrays, which cannot work.

Reproduction (issue):
```python
col = fits.Column('a', format='QD', array=[[0], [0, 0]])
fits.BinTableHDU.from_columns([col]).writeto('diffbug.fits')
fits.FITSDiff('diffbug.fits', 'diffbug.fits')   # ValueError before the fix
```

## Fix
- `astropy/io/fits/diff.py`: treat both `P` and `Q` formats as variable-length arrays (`"P" in col.format or "Q" in col.format`).
- `astropy/io/fits/tests/test_diff.py`: `test_vla_identical_and_different` (parametrized over `PD` and `QD`) checks a file is identical to itself and that a changed element is reported as one differing row. The `QD` case fails before the change with the ValueError above.
- Changelog `docs/changes/io.fits/14600.bugfix.rst` (number is a placeholder to be renamed to the real PR number).

## Verification
`/opt/miniconda3/envs/testbed/bin/python -m pytest astropy/io/fits/tests/test_diff.py -k vla_identical -p no:cacheprovider -q` : fails on base (QD), passes after. Whole `test_diff.py`: 50 passed.
