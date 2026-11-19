Fix one-sample shift in centered even-window rolling on dask arrays

## Overview
For chunked (dask) data, `rolling(center=True)` with an even window of 4 or more (4, 6, 8, ...) returned values shifted by one sample compared with the same calculation on in-memory data. Length and coordinates were right, so only the values were off.

## Cause
In `dask_array_ops.rolling_window`, the front of the array is padded up to the overlap depth and the result is then cropped. The crop used `drop_size = depth - pad_size + 1`, one sample too many, so every window sat one step later than numpy's. The correct value is `depth - pad_size`, which is exactly the extra padding added.

## Changes
- `xarray/core/dask_array_ops.py`: `drop_size = depth[axis] - pad_size`.
- `test_duck_array_ops.py::test_dask_rolling`: add windows 4 and 6 (8 was already covered and also failed).
- `test_dataarray.py::test_rolling_construct_dask_even_window_center`: chunked vs in-memory `rolling(center=True).construct()` and `.mean()`.
- `doc/whats-new.rst` entry.

## Verification
- Before the fix: `test_dask_rolling` fails for center=True with windows 4, 6, 8; the new DataArray test fails for windows 4 and 6.
- After: `pytest xarray/tests/test_duck_array_ops.py xarray/tests/test_dataarray.py -k rolling` gives 457 passed; adding test_dataset.py gives 1013 passed, 16 skipped.
