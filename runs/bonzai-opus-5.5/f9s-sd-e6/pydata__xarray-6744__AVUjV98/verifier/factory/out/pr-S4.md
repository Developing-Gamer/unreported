Fix DataArrayRolling.__iter__ ignoring `center`

## Overview
Iterating manually over `da.rolling(x=3, center=True)` yielded trailing windows, ignoring `center`, so the windows disagreed with `rolling(...).mean()` by half a window. `__iter__` now offsets window bounds when `center=True`.

## Details
- `DataArrayRolling.__iter__` used `stops = arange(1, n+1)` regardless of `self.center`. It now uses `offset = (window + 1) // 2` when centered (else 1), matching the centering used by the reduction path; starts are clipped to 0 at the left edge and `isel` clips stops at the right edge. `min_periods` masking is unchanged.
- Tests: `test_rolling_iter` is parametrized over `center`; new `test_rolling_iter_matches_reduction` compares iterated window means with `rolling().mean()` for window 3/4, center on/off, min_periods None/1.
- whats-new entry added.

## Proof
Before (base): 4 failures, e.g. `test_rolling_iter_matches_reduction[3-True]` — NaN positions `[T,T,T,F,...]` vs expected `[T,T,F,...,F,T]`.
After: `pytest xarray/tests/test_rolling.py` — 1802 passed, 32 skipped, 4 xpassed.

## Verification
`python -m pytest xarray/tests/test_rolling.py`
