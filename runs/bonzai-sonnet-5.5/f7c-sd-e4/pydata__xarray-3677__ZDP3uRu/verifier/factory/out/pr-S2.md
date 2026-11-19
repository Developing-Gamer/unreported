Only unwrap pandas/xarray containers' `.values` in as_compatible_data

## Overview
`arr.loc[{'dim_0': 0}] = obj` replaced any `obj` that has a `values` attribute with that attribute, so object-dtype arrays could not store such objects (`array([array(5)], dtype=object)` instead of the object).

## Cause
`as_compatible_data` ran `data = getattr(data, "values", data)` on every input, and `Variable.__setitem__` sends all non-Variable values through it.

## Fix
- `as_compatible_data` returns `.data` for `Variable` and `DataArray`.
- The generic `.values` unwrap now applies only to `pd.Series`, `pd.Index` and `pd.DataFrame`.
- Test `TestVariable.test_setitem_object_with_values_attribute` (Variable and `DataArray.loc`); whats-new entry.

## Verification
- New test fails on the base commit and passes with the fix.
- `pytest xarray/tests/test_variable.py test_dataarray.py test_dataset.py test_sparse.py test_computation.py`: same 11 pre-existing failures before and after (dask rolling, cftime trapz, sparse); everything else passes, plus the new test.
