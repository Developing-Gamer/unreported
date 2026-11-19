Fix off-by-one in dask centered rolling window for even window sizes

## Root cause
In `dask_array_ops.rolling_window`, when padding smaller than the overlap depth was enlarged, `drop_size = depth - pad_size + 1` trimmed one element too many. With `center=True` and an even window (e.g. 4) on a dask-backed (large) array, results were shifted one sample relative to the numpy path (small extracts).

## Change
Use `drop_size = depth[axis] - pad_size` (xarray/core/dask_array_ops.py). Added `test_rolling_construct_dask_matches_numpy` covering windows 2-6, center on/off, several chunk sizes, for `construct` and `mean`.

## Verification
Dask and numpy results now agree for windows 2-8 and several chunkings. Previously failing `test_rolling_wrapped_dask[8-*-True-*]` and `test_dask_rolling[True-8-*]` now pass.
