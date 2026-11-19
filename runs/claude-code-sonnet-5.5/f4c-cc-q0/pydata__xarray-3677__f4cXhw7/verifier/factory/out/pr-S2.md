Don't coerce arbitrary objects with a `values` attribute in Variable assignment

## Root cause
`as_compatible_data` did `getattr(data, "values", data)` on any input, so `var[idx] = obj` stored `obj.values` for any object that happened to have a `values` attribute (e.g. lmfit `ModelResult`).

## Change
In xarray/core/variable.py only `DataArray` and pandas `Series`/`DataFrame`/`Index` are unwrapped via `.values`; other objects are kept as-is. Added `test_setitem_object_with_values_attribute`.

## Verification
The S2 repro now stores the `HasValues` instance. test_variable, test_dataarray, test_dataset, test_dask show no new failures against the baseline.
