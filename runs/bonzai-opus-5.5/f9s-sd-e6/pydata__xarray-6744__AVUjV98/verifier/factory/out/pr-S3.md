Fix DataArray.__setitem__ / .loc assignment ignoring dimension order of a DataArray value

## Overview
Assigning a DataArray whose dimensions are in a different order than the target (`da[...] = value` or `da.loc[...] = value`) silently laid the values out by position. On square grids the shapes match, so no error was raised: the diagonal stayed right and every off-diagonal cell received its transposed neighbour's value. Values are now aligned by dimension name.

## Cause
`DataArray.__setitem__` checked coordinate consistency for a DataArray value but passed the DataArray itself to `Variable.__setitem__`. That method only aligns by dimension name for a `Variable`; anything else goes through `as_compatible_data` and is matched by position.

## Fix
After `assert_coordinate_consistent`, use `value = value.variable` so the dimension names reach `Variable.__setitem__`.

## Verification
- New test `test_setitem_dataarray_transposed_value` (square via `[...]`, `.loc`, dict key; and non-square 2x3 given as 3x2): fails on the base commit (off-diagonal values transposed), passes with the fix.
- `pytest xarray/tests/test_dataarray.py xarray/tests/test_variable.py xarray/tests/test_indexing.py`: 990 passed, 59 skipped, 21 xfailed, 24 xpassed.
