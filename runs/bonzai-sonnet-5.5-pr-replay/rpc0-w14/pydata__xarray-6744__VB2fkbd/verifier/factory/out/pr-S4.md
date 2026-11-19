Respect `center` when iterating over DataArrayRolling

## Overview
`for label, window in da.rolling(x=3, center=True)` produced trailing windows (as if `center=False`), so manual iteration disagreed with `.mean()`/`.construct()`. `DataArrayRolling.__iter__` now applies the centering offset.

## Evidence
GitHub issue (discussion #6738): the `center` kwarg is ignored when manually iterating over a DataArrayRolling.

## Details
- `xarray/core/rolling.py`: `__iter__` uses `offset = (window + 1) // 2 if center else 1`, `stops = arange(offset, n + offset)`, `starts = max(stops - window, 0)`. Slicing beyond the end truncates the trailing windows.
- Added `test_rolling_iter_center` (windows 2-5, center True/False, min_periods None/1) comparing the mean of iterated windows to `rolling(...).mean()`. On the base commit 6 cases (center=True, window 3-5) fail; after the fix all pass.
- whats-new entry added.

## Verification
- `python -m pytest xarray/tests/test_rolling.py -k rolling_iter -q`
- Full `xarray/tests/test_rolling.py`: 1806 passed, 32 skipped, 4 xpassed.
