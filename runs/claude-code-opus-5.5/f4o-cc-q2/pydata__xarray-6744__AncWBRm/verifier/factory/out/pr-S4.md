Fix DataArrayRolling iteration ignoring `center=True`

## Root cause
`DataArrayRolling.__iter__` computed window bounds as `stops = arange(1, n + 1)` and
`starts = stops - window`, which are always trailing (right-aligned) windows. The
`center` setting was never consulted, so manually iterating a centered rolling
object yielded windows shifted relative to `rolling(..., center=True).mean()`
(GH6738/GH6739).

## Change
In `xarray/core/rolling.py`, the stop offset is now `(window + 1) // 2` when
`center` is true for the rolling dimension (and 1 otherwise), matching the
alignment used by the reduction methods. Starts that would be negative are clipped to 0.
The `min_periods` masking is unchanged, so incomplete windows at both edges are
still masked.

## Verification
- Reproducer from the issue now gives `[nan, 2.0, ..., 8.0, nan]`, which matches `.mean()`.
- Added `TestDataArrayRolling.test_rolling_iter_center`, parametrized over
  center ∈ {True, False}, window ∈ {1..4}, min_periods ∈ {None, 1}. It compares
  the means of the iterated windows to `rolling().mean()`. 4 cases fail without the fix and all pass with it.
- `pytest xarray/tests/test_rolling.py`: 1806 passed, 32 skipped, 4 xpassed.
