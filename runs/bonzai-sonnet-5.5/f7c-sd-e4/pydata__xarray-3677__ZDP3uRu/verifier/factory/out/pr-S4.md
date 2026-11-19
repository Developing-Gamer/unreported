Fix Dataset.merge failing when given a DataArray

## Overview
`xr.merge([ds, da])` works, but `ds.merge(da)` raised `AttributeError: 'DataArray' object has no attribute 'items'`. `Dataset.merge` documents `other` as castable to Dataset, so a named DataArray should be accepted.

## Cause
`dataset_merge_method` passed `other` straight to `merge_core` (and to `other.items()` when `overwrite_vars` is set). Only the top-level `merge()` converted DataArrays with `to_dataset()`.

## Fix
Convert a DataArray `other` with `to_dataset()` in `dataset_merge_method`. An unnamed DataArray raises the usual "unable to convert unnamed DataArray" ValueError. Docstring and whats-new updated.

## Verification
- New test `xarray/tests/test_merge.py::TestMergeMethod::test_merge_dataarray` fails before (AttributeError), passes after.
- `pytest xarray/tests/test_merge.py`: 22 passed.
