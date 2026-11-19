Fix FITSDiff reporting differences for identical files with 'Q' format variable-length array columns

## Root cause
`TableDataDiff._diff` (astropy/io/fits/diff.py) compares variable-length array (VLA)
columns row by row with `np.allclose`, but it only took that path when `"P" in col.format`.
VLA columns with 64-bit descriptors use the `Q` format (e.g. `QD`). They fell through to
`np.where(arra != arrb)`, which runs on an object array of per-row ndarrays. Depending on
row lengths this either flags identical rows as different or raises
`ValueError: The truth value of an array ... is ambiguous` (current numpy).

## Change
Treat `Q` format columns the same as `P` format columns in the VLA comparison branch:
`elif "P" in col.format or "Q" in col.format:`.

## Verification
- Reproduced the issue example (`Column('a', format='QD', array=[[0], [0, 0]])`, file
  compared to itself). Before the fix it raised `ValueError`; after the fix `FITSDiff(...).identical`
  is `True`.
- Added `TestTableDataDiff::test_identical_files_q_format_vla` in
  astropy/io/fits/tests/test_diff.py. It checks that a file compared to itself is identical and
  that a real difference in a `Q` column is still reported (row index and count). It fails
  without the fix and passes with it.
- `pytest astropy/io/fits/tests/`: 987 passed. The single failure,
  `test_fitstime.py::test_time_to_fits_loc[Table]`, is a leap-second auto-update warning
  caused by the sandbox having no network access and is unrelated to this change.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
