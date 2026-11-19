Fix assert_allclose ignoring dimension order

## Overview
`xarray.testing.assert_allclose` compared dimension names as unordered sets and then compared raw values by position. A square array with its axes swapped (e.g. dims `('x','y')` vs `('y','x')` over the same buffer) therefore passed validation even though off-diagonal cells differ. Non-square arrays failed on shape mismatch, which hid the bug. Reported in data-export-support: "Validation still reports success for the exported square grids, but off-diagonal cells differ from the source."

## Details
- `xarray/testing.py`: `compat_variable` now uses `a.dims == b.dims` (ordered), consistent with `Variable.equals`/`assert_equal`.
- `xarray/tests/test_testing.py`: new `test_assert_allclose_dim_order` (Variable, DataArray, Dataset) with a 4x4 array and swapped dims; it failed (DID NOT RAISE AssertionError) before the fix.
- `doc/whats-new.rst`: bug-fix entry.

## Verification
- Before: `python -m pytest xarray/tests/test_testing.py -k dim_order` -> 3 failed (DID NOT RAISE).
- After: passes; plus test_testing, test_variable, test_dataarray, test_dataset, test_computation, test_groupby, test_missing, test_interp, test_duck_array_ops: 2946 passed, 0 failed.
