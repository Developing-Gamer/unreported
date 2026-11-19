Respect `center` when iterating over DataArrayRolling

## Overview
`for label, window in da.rolling(x=3, center=True)` ignored `center`: `DataArrayRolling.__iter__` always built trailing windows, so the iterated windows disagreed with `rolling(..., center=True).mean()` by half a window (pydata/xarray discussion #6738).

## Details
- `__iter__` now computes `offset = (window + 1) // 2` when `center` is set (else 1), so window stops are `arange(offset, n + offset)`, starts are `stops - window` clipped to 0; `isel` slicing clips stops past the end. `min_periods` masking is unchanged.
- Tests: `test_rolling_iter` is parametrized over `center`; new `test_rolling_iter_matches_reduction` compares iterated window means with `rolling(...).mean()` for windows 3 and 4, centered and not.
- Added a whats-new entry.

## Verification
- Before the fix: 4 failures (`center=True` cases). After: `pytest xarray/tests/test_rolling.py` -> 1798 passed, 32 skipped, 4 xpassed.
