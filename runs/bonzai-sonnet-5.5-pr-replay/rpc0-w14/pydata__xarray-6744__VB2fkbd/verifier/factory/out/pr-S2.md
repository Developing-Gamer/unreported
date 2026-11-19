No pull request: Dataset.merge(DataArray) already works on this commit

The issue reports that `ds.merge(da)` fails while `xr.merge([ds, da])` works. On the starting commit this no longer reproduces.

- `Dataset.merge` (xarray/core/dataset.py, ~line 4782) already converts a DataArray with `other.to_dataset()` before calling `dataset_merge_method`, and its signature accepts `CoercibleMapping | DataArray`.
- `xarray/tests/test_merge.py::TestMergeMethod::test_merge_dataarray` already exists and passes on the base commit.
- Manual check: `ds.merge(da)` and `ds.merge(da, overwrite_vars="b")` both return the same dataset as `xr.merge([ds, da])`. An unnamed DataArray raises "unable to convert unnamed DataArray to a Dataset without providing an explicit name".

Since no test fails on the base commit, no change was made.
