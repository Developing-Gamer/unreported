Fix Dataset.merge with a DataArray argument (S4, S6)

## Root cause
`xr.merge` converts DataArray inputs to Datasets, but `Dataset.merge` passed `other` straight to `dataset_merge_method`/`coerce_pandas_values`, which calls `other.items()`. A DataArray has no `items`, so it raised `AttributeError` (472 Sentry events in S6, same stack as the S4 issue).

## Change
`Dataset.merge` now calls `other.to_dataset()` when `other` is a `DataArray` (xarray/core/dataset.py). Added `test_merge_dataarray_method` in test_merge.py.

## Verification
Repro from S4 now returns the same result as `xr.merge([ds, da])`. test_merge, test_dataset, test_combine pass apart from pre-existing, unrelated cftime failures.
