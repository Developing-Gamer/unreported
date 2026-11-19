Add keep_attrs to xr.where so the result can keep the attrs of x

## Overview
`xr.where(cond, x, y)` always dropped attributes: it called `apply_ufunc` without `keep_attrs`, which falls back to the global option (default False, so `"drop"`). There was no way to keep `x`'s attrs (units etc.). Turning on the global option did not help either, because `"override"` copies the attrs of the first argument, which is `cond`.

## Details
- `xr.where` gets a `keep_attrs=None` parameter, resolved against the global `keep_attrs` option and passed to `apply_ufunc`.
- When it resolves to `True`, the result's attrs are set to a copy of `x`'s attrs (`{}` if `x` is a scalar), consistent with `DataArray.where`/`Dataset.where`. They are set on the result rather than through a callable passed to `apply_ufunc`, because that callable would also be applied to coordinate attrs.
- Default behaviour (attrs dropped) is unchanged.
- Docstring and `doc/whats-new.rst` updated.

## Before / After
Before: `xr.where(cond, x, y, keep_attrs=False)` raises `TypeError: where() got an unexpected keyword argument 'keep_attrs'`, and there is no way to keep `x`'s attrs.
After: `xr.where(cond, x, y, keep_attrs=True).attrs == x.attrs`, also under `set_options(keep_attrs=True)`.

## Verification
- New `test_where_attrs` in `xarray/tests/test_computation.py` fails on the base commit (`TypeError ... unexpected keyword argument 'keep_attrs'`) and passes with the fix; it covers DataArray, Dataset, scalar `x`, True/False/default and the global option.
- `pytest xarray/tests/test_computation.py`: 248 passed, 1 skipped.
