Fix DataArrayRolling iteration ignoring `center=True`

Root cause: `DataArrayRolling.__iter__` always built trailing windows (`stop = i + 1`, `start = stop - window`) and never looked at `self.center`. Manual iteration over `da.rolling(x=3, center=True)` therefore yielded windows shifted relative to the result of `.mean()` and other reductions.

Change: in `xarray/core/rolling.py`, `__iter__` now uses an offset of `(window + 1) // 2` when the dimension is centered (1 otherwise) to compute window stops, and clips the leading starts to 0. The windows now match the ones used by the reduction methods, including for even window sizes. The number of windows is taken from `obj.sizes[dim]`.

Verification: added `test_rolling_iter_center` in `xarray/tests/test_rolling.py`. It compares the per-window mean from iteration with `rolling(...).mean()` for window sizes 1-4, with center True and False. The full `test_rolling.py` suite passes (1798 passed). The issue example now gives `[nan, 2, 3, ..., 8, nan]`.
