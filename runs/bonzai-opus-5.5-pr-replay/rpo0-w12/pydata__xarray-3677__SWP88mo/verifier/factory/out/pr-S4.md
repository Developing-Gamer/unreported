Fix Dataset.merge failing when `other` is a DataArray

## Overview
`xr.merge([ds, da])` accepts a named DataArray, but `ds.merge(da)` raised `AttributeError: 'DataArray' object has no attribute 'items'`. `Dataset.merge` now converts a DataArray `other` to a Dataset, as the top-level `merge` does.

## Details
- `dataset_merge_method` (xarray/core/merge.py) passed `other` straight to `merge_core`, where `coerce_pandas_values` treated the DataArray as a mapping and called `.items()`. It now calls `other.to_dataset()` for a DataArray first (before the `overwrite_vars` handling, so that also works).
- Docstring of `Dataset.merge` and whats-new updated.
- Unnamed DataArrays still raise the existing `to_dataset` ValueError.

## Verification
- New test `TestMergeMethod::test_merge_dataarray` fails before the fix with `AttributeError: 'DataArray' object has no attribute 'items'` and passes after.
- `pytest xarray/tests/test_merge.py xarray/tests/test_dataset.py -k merge`: 25 passed.
