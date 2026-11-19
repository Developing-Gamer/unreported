No pull request: Dataset.merge(DataArray) already works at this commit

Issue: `ds.merge(da)` with a named DataArray reportedly fails with `AttributeError: 'DataArray' object has no attribute 'items'`.

At the starting commit this does not reproduce. `Dataset.merge` (xarray/core/dataset.py, ~line 4780) already does `other = other.to_dataset() if isinstance(other, DataArray) else other` before calling `dataset_merge_method`, and the type hint is `CoercibleMapping | DataArray`. The regression test `TestMergeMethod.test_merge_dataarray` in xarray/tests/test_merge.py already exists and passes.

Checked: `ds.merge(da)` equals `xr.merge([ds, da])` for 0-d and 1-d DataArrays, also with `overwrite_vars` as a name that is in the DataArray, one that is not, and a list. All succeed. No code change made.
