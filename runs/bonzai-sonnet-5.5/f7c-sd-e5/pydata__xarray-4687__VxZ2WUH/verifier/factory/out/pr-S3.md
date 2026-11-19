xr.where: add keep_attrs and keep the attributes of x

## Overview
`xr.where(cond, x, y)` always returned a result without attributes, because it called `apply_ufunc` without `keep_attrs` and the default is to drop. It had no `keep_attrs` argument and ignored `set_options(keep_attrs=True)`. This adds `keep_attrs` to `xr.where` (default `None`, which follows the global option, which defaults to False). When true, the result takes the attrs of `x`, as `DataArray.where` and `Dataset.where` do, rather than those of `cond`.

## Details
- `keep_attrs=True` runs `apply_ufunc` with `"override"`, then sets the result's attrs from `x`. For a Dataset `x` the data variable attrs also come from `x`. A scalar `x` gives empty attrs. I did not use a callable `keep_attrs` that returns `x.attrs`: `apply_ufunc` also uses it for coordinate and variable attrs, so it overwrote coordinate attrs with the attrs of `x`.
- The default is unchanged (attrs dropped).
- Docstring and `doc/whats-new.rst` updated.

## Reproduction / verification
- `pytest xarray/tests/test_computation.py -k test_where_attrs`. Before the fix it fails with `TypeError: where() got an unexpected keyword argument 'keep_attrs'`. After the fix it passes.
- `pytest xarray/tests/test_computation.py`: 248 passed, 1 skipped.
