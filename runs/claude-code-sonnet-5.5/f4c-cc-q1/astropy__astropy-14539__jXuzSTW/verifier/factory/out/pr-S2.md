Fix FITSDiff reporting spurious differences for Q-format variable-length array columns

Root cause: `TableDataDiff._diff` only used the element-wise VLA comparison (`np.allclose` per row) when `"P" in col.format`. Columns with 64-bit descriptors (`Q`, e.g. `QD`) fell through to `np.where(arra != arrb)`, which on object arrays of ragged arrays either gives wrong results or raises "truth value of an array ... is ambiguous". So a file compared to itself could be reported as different.

Change: treat both `P` and `Q` formats as VLAs in `astropy/io/fits/diff.py`. Added a regression test (`test_fitsdiff_vla_q_format_identical`) and a changelog entry.

Verification: reproduced the issue's script before the change (ValueError) and confirmed `FITSDiff(f, f).identical` is True afterwards; `pytest astropy/io/fits/tests/test_diff.py` passes (49 tests), including a check that a real difference in a QD column is still detected.
