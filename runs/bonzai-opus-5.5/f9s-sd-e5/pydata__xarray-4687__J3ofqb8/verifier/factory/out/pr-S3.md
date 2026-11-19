Add keep_attrs argument to xr.where

## Overview
`xr.where` called `apply_ufunc` without `keep_attrs`, so it always used the global option (default False) and dropped the attributes of its inputs (e.g. `units`). Unlike `DataArray.where`, there was also no way to keep them. This adds a `keep_attrs` argument to `xr.where`. With `keep_attrs=True`, or the global option set, the result takes the attrs of `x`. The default is unchanged: it follows the global `keep_attrs` option.

## Details
- `xarray/core/computation.py`: `where(cond, x, y, keep_attrs=None)`. `None` resolves to `_get_keep_attrs(default=False)`. `True` becomes a callable returning `x.attrs`, since the default `"override"` would take the attrs of the first argument, `cond`.
- Tests: new `test_where_attrs` covers the default, the global option, `keep_attrs=True/False`, and `cond` carrying different attrs than `x`.
- `doc/whats-new.rst` entry added.

## Verification
- `pytest xarray/tests/test_computation.py -k where_attrs`: failed on the base commit (with the global option set, attrs were `cond`'s, not `x`'s) and passes now.
- `pytest xarray/tests/test_computation.py xarray/tests/test_units.py -k where`: 132 passed.
- test_dataarray.py and test_dataset.py fail at collection on an unrelated pandas ImportError in this environment.
