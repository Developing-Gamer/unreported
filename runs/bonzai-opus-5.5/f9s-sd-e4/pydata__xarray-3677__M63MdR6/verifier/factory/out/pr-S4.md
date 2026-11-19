Fix Dataset.merge failing when `other` is a DataArray

## Overview
`xr.merge([ds, da])` works with a named DataArray, but `ds.merge(da)` raised `AttributeError: 'DataArray' object has no attribute 'items'`. `dataset_merge_method` passed the DataArray to `merge_core`, which treated it as a mapping. It now converts a DataArray `other` to a Dataset first, as the top-level `merge` does.

## Details
- `xarray/core/merge.py`: `dataset_merge_method` calls `other.to_dataset()` for a DataArray, before the `overwrite_vars` handling (which also uses `other.items()`/`set(other)`).
- `xarray/core/dataset.py`: docstring says `other` may be a DataArray.
- `doc/whats-new.rst`: entry added.
- `xarray/tests/test_merge.py`: `TestMergeMethod.test_merge_dataarray` covers plain merge and `overwrite_vars`.

## Verification
- `python -m pytest xarray/tests/test_merge.py -k test_merge_dataarray` failed with AttributeError before the fix, passes after.
- `pytest xarray/tests/test_merge.py xarray/tests/test_dataset.py -k merge`: 25 passed.
