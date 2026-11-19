Respect `center` when iterating over DataArrayRolling

## Overview
`for label, window in da.rolling(time=w, center=True)` yielded trailing windows, as if `center=False`, so the windows disagreed with `.mean()` / `.construct()`. `DataArrayRolling.__iter__` now applies the centering offset, so iterated windows match the aggregation methods (odd and even window sizes). Reported in the GitHub issue "center kwarg ignored when manually iterating over DataArrayRolling" (discussion #6738).

## Details
- `xarray/core/rolling.py`: `__iter__` used `stops = arange(1, n+1)` regardless of `center`. It now uses `offset = (window + 1) // 2 if center else 1`, `stops = arange(offset, n + offset)`, `starts = stops - window`, and clamps the leading starts to 0. Slicing past the end truncates safely.
- Test `test_rolling_iter_center` (centre True/False, windows 3, 4, 7, numpy and dask) compares the mean of each iterated window to `rolling(...).mean()`.
- `doc/whats-new.rst` entry added.

## Verification
- Before the fix: the 6 `center=True` cases of the new test fail, e.g. the iterated window mean has values where the rolling mean is NaN. The 6 `center=False` cases pass.
- After the fix: `pytest xarray/tests/test_rolling.py` gives 1802 passed, 32 skipped, 4 xpassed.
