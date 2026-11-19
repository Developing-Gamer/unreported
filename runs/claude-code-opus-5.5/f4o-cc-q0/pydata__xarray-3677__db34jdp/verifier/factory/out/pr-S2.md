Only unwrap `.values` from pandas/xarray objects in `as_compatible_data`

Root cause
----------
`xarray.core.variable.as_compatible_data` did `data = getattr(data, "values", data)` to avoid
storing nested self-described arrays. That unwraps *any* object with a `values` attribute, so
assigning, e.g., an lmfit `ModelResult` (or any object with `.values`) into an object-dtype
array via `Variable.__setitem__` / `DataArray.loc[...] = obj` stored `obj.values` instead of `obj`.

Change
------
- Unwrap only `pd.Series` / `pd.DataFrame` via `.values` (`pd.Index` is already handled earlier
  through `NON_NUMPY_SUPPORTED_ARRAY_TYPES`).
- Handle `DataArray` explicitly alongside `Variable` by returning its `.data`, so xarray objects
  are still unwrapped (and dask-backed DataArrays are no longer eagerly computed).
- Arbitrary objects are now stored as-is.

Verification
------------
- New test `TestVariable.test_setitem_object_with_values_attribute` (xarray/tests/test_variable.py)
  fails before the change and passes after.
- The issue's snippet now gives `array([<HasValues object>], dtype=object)`.
- Ran test_variable, test_dataarray, test_dataset, test_indexing, test_dask, test_merge,
  test_combine, test_concat, test_missing, test_duck_array_ops, test_extensions: no new failures
  compared with the base commit (the remaining failures were already failing before this change
  and come from cftime/dask version incompatibilities in the environment).
