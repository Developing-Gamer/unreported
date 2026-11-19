Add `keep_attrs` to `xr.where` so attributes can be preserved

## Root cause

`xr.where(cond, x, y)` (`xarray/core/computation.py`) calls `apply_ufunc` without a
`keep_attrs` argument, and it has no way for callers to pass one. `apply_ufunc` defaults
to `keep_attrs=False`, so the result always loses its attributes. Unlike `DataArray.where`
and `Dataset.where`, which keep the attrs of the object being masked, users could not opt in.

## Change

- `xr.where` gets a new `keep_attrs=None` argument. `None` falls back to the global
  `xr.set_options(keep_attrs=...)` option, which is `False` by default, so existing behaviour
  doesn't change.
- When `keep_attrs` is true, the result takes the attributes of **`x`**, the second argument.
  This matches `DataArray.where` and `Dataset.where`, where `self` plays the role of `x`.
  For a Dataset result, the dataset attrs and each data variable's attrs come from the
  matching entries of `x`. If `x` is a scalar or array, there are no attrs to keep and the
  result has empty attrs.
- When `keep_attrs` is true, coordinate attrs are also kept (the merge uses `"override"`
  instead of `"drop"`).

Note on the issue's examples: both pass a scalar as `x`, for example
`xr.where(da == 0, -1, da)`. Under the documented rule above (keep the attrs of `x`), they
still give `{}`. To keep the attributes, put the DataArray in the `x` position:
`xr.where(da != 0, da, -1, keep_attrs=True)`. The method form `da.where(da != 0, -1)` also
works.

## Verification

- New test `xarray/tests/test_computation.py::test_where_attrs` covers:
  - the default (attrs dropped);
  - `keep_attrs=True` and the global option (attrs of `x` kept, not those of `cond` or `y`);
  - the issue's scenario with the DataArray as `x`;
  - a scalar `x`;
  - Dataset inputs.
- The test fails without the library change and passes with it.
- `pytest xarray/tests/test_computation.py`: 248 passed, 1 skipped.
- `pytest --doctest-modules xarray/core/computation.py`: 6 passed.

The dtype remark in the first issue (int8 becoming int64) is numpy's type promotion with
Python int scalars, not something xarray controls, so it is not changed here.
