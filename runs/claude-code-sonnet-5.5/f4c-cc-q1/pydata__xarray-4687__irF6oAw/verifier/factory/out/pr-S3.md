Add keep_attrs to xr.where

Root cause: `xr.where` called `apply_ufunc` without `keep_attrs`, so attrs were always dropped and the caller had no way to keep them (S3).

Change: `where(cond, x, y, keep_attrs=None)`. None follows the global `keep_attrs` option (default False, so existing behavior is unchanged). True keeps the attrs of `x`, consistent with `DataArray.where`/`Dataset.where`. Strings/callables are passed through to `apply_ufunc`. Note that the attrs come from `x`, so the second example in the issue (attrs on `y` only) gets empty attrs. The dtype promotion mentioned in the issue comes from numpy and is not addressed. Added `test_where_attrs`.

Verification: `pytest xarray/tests/test_computation.py xarray/tests/test_plugins.py` passes.
