Allow `Dataset.merge` to accept a `DataArray` (fixes S4, S6)

Root cause
----------
`xr.merge([ds, da])` converts DataArrays to Datasets, but `Dataset.merge` passed `other`
directly to `dataset_merge_method` -> `merge_core` -> `coerce_pandas_values`, which treats any
non-Dataset as a mapping and calls `obj.items()`. `DataArray` has no `items`, so it raises
`AttributeError: 'DataArray' object has no attribute 'items'`. This is the same failure
reported in the GitHub issue (S4) and in the production Sentry event (S6, 472 events).

Change
------
In `Dataset.merge` (xarray/core/dataset.py), convert a `DataArray` `other` with
`other.to_dataset()` before calling `dataset_merge_method`, matching the top-level `xr.merge`.

Verification
------------
- New test `TestMergeMethod.test_merge_dataarray` asserts `ds.merge(da)` is identical to
  `xr.merge([ds, da])`; fails before, passes after.
- The issue's example now returns a Dataset with both `a` and `b`.
- Broader test run (merge/dataset/dataarray/combine/concat/...) shows no new failures.
