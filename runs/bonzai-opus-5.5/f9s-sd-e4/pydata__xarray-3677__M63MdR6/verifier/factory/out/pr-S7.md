Fix one-sample shift in centered even-window rolling on dask arrays

## Overview
`da.chunk(...).rolling(t=4, center=True).mean()` returned results shifted by one sample compared with the in-memory result (the same calculation on a small, unchunked extract). Timestamps and shapes matched, so it was easy to miss. Dask and numpy now agree.

## Details
In `rolling_window` (`xarray/core/dask_array_ops.py`), when a centered even window needs front padding smaller than the overlap depth, the array is padded up to `depth` and then cropped by `drop_size`. `drop_size` was `depth - pad_size + 1`, which cropped one element too many; the correct value is `depth - pad_size`. (window=4, center=True: depth=2, pad_size=1, so drop 1, not 2.)

Tests: added window=4 to `test_dask_rolling` and `test_rolling_wrapped_dask`. Together with the existing window=8 cases, these failed before the fix (12 failures) and pass after. Added a whats-new entry.

## Verification
`python -m pytest xarray/tests/test_duck_array_ops.py xarray/tests/test_dataarray.py xarray/tests/test_dask.py -k rolling -q` — before: 12 failed; after: 464 passed.
