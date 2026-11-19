Fix Dataset.merge failing when given a DataArray

## Overview
`xr.merge([ds, da])` works, but `ds.merge(da)` raised `AttributeError: 'DataArray' object has no attribute 'items'`. `Dataset.merge` passed the DataArray straight to `merge_core`, which treats non-Datasets as mappings. `ds.merge(da)` now gives the same result as `xr.merge([ds, da])`.

## Details
- `dataset_merge_method` (xarray/core/merge.py) converts a DataArray `other` with `to_dataset()` first, as the top-level `merge()` does. This also covers the `overwrite_vars` branch, which calls `other.items()`. An unnamed DataArray raises the usual "without providing an explicit name" ValueError.
- Docstring of `Dataset.merge` now lists DataArray; whats-new entry added.
- Test: `TestMergeFunction.test_merge_dataarray_method` in xarray/tests/test_merge.py. It failed before with the AttributeError above.

## Verification
`python -m pytest xarray/tests/test_merge.py xarray/tests/test_dataset.py -k merge` — 25 passed.
