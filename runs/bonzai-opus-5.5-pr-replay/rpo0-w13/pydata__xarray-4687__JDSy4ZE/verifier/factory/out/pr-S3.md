Add keep_attrs argument to xr.where

## Overview
`xr.where(cond, x, y)` dropped all attributes (e.g. `units`) of its inputs, unlike `DataArray.where`, because it called `apply_ufunc` without `keep_attrs` and so fell back to the global default (`False` -> `"drop"`). `xr.where` now accepts `keep_attrs`; with `keep_attrs=True` the result carries the attrs of `x`. When omitted it follows the global `keep_attrs` option (default still drops, so no behaviour change unless opted in).

## Details
- `xarray/core/computation.py`: new `keep_attrs=None` parameter, documented. `None` resolves via `_get_keep_attrs(default=False)`; `True` becomes a callable returning `getattr(x, "attrs", {})` (so a scalar `x` gives no attrs and `cond`'s attrs are never used).
- `doc/whats-new.rst`: entry added.
- Test `test_where_attrs` in `xarray/tests/test_computation.py`.

## Proof
Before: `xr.where(cond, x, y, keep_attrs=True)` -> `TypeError: where() got an unexpected keyword argument 'keep_attrs'` (test_where_attrs fails). After: passes.

## Verification
`python -m pytest xarray/tests/test_computation.py xarray/tests/test_duck_array_ops.py` passes. test_dataarray/test_dataset cannot be collected in this environment (pandas `UndefinedVariableError` import error, unrelated).
