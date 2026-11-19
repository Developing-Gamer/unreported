Stop as_compatible_data from replacing arbitrary objects with their `.values` attribute

## Overview
`as_compatible_data` ran `getattr(data, "values", data)` on every input, so any user object with a `values` attribute was replaced by that attribute. `Variable.__setitem__` (and so `DataArray.loc[...] = obj`) therefore stored `5` instead of the object in an object-dtype array when `obj.values == 5`.

## Evidence
GitHub issue "Variable.__setitem__ coercing types on objects with a values property": `bad_indexed.loc[{'dim_0': 0}] = HasValues()` gave `array([array(5)], dtype=object)` instead of the instance.

## Details
- `as_compatible_data` now unwraps only known containers: `Variable` and `DataArray` (via `.data`, which keeps dask-backed arrays lazy), and `pd.Series`/`pd.DataFrame` (via `.values`). `pd.Index` was already handled earlier in the function.
- New test `TestVariable.test_setitem_object_with_values_attribute` covers `Variable.__setitem__` and `DataArray.loc` assignment. It fails before the change and passes after.
- whats-new entry added.

## Verification
- `python -m pytest xarray/tests/test_variable.py -k values_attribute`: failed before, passes after.
- test_variable, test_dataarray, test_dataset, test_indexing, test_sparse, test_duck_array_ops, test_computation: 15 failures, identical to the 15 on the base commit (cftime, dask rolling, sparse `where`; unrelated).
