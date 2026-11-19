Fix off-by-one in dask `rolling_window` for centered even-sized windows

Root cause
----------
`xarray.core.dask_array_ops.rolling_window` pads the array before overlapping when the
required padding is smaller than the overlap depth, then crops `drop_size` leading elements.
`drop_size` was computed as `depth - pad_size + 1`, cropping one element too many. This only
happens when `pad_size` is between 0 and the depth, which is the case for `center=True` with
an even window (e.g. 4 or 8). So dask-backed (chunked, "large data") results were shifted by one
sample relative to the numpy path, while shapes and coordinates stayed the same. That matches the
report of a centered four-sample trend that is one sample out of alignment between the large
export and a small extract, with timestamps and row counts unchanged.

Change
------
`drop_size = depth[axis] - pad_size` (removed the spurious `+ 1`).

Verification
------------
- Script comparing `rolling(t=w, center=c).mean()` on numpy vs. chunked dask for w in
  {2,3,4,5,8}: windows 4 and 8 with center=True differed before and all match after.
- Existing tests `test_rolling_wrapped_dask[8-*-True-*]` (4 cases) and
  `test_dask_rolling[True-8-*]` (2 cases) failed on the base commit and now pass. Added window
  size 4 to `test_dask_rolling`'s parametrization to cover the reported case.
- No new failures in the broader test run.
