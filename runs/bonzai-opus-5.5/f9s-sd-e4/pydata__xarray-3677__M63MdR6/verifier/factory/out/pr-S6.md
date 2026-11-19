Fix Dataset.merge failing when `other` is a DataArray

Not opened: open PR #1001 already contains this exact fix (see Details).

## Overview
`xr.merge([ds, da])` works with a named DataArray, but `ds.merge(da)` raised `AttributeError: 'DataArray' object has no attribute 'items'` (Sentry ev_s6, 472 events / 107 users in 7 days). `dataset_merge_method` passed the DataArray to `merge_core`, which treated it as a mapping.

## Details
- Fix: `dataset_merge_method` in `xarray/core/merge.py` converts a DataArray `other` with `to_dataset()` before the `overwrite_vars` handling. The investigation proposed doing this in `Dataset.merge`; `dataset_merge_method` is the better place because `overwrite_vars` handling there also iterates `other`.
- Test: `TestMergeMethod.test_merge_dataarray` in `xarray/tests/test_merge.py`.
- An unnamed DataArray still raises the clear ValueError from `to_dataset()`.

## Verification
- `python -m pytest xarray/tests/test_merge.py -k test_merge_dataarray` on the base commit: fails with `AttributeError: 'DataArray' object has no attribute 'items'`.
- With the fix, `pytest xarray/tests/test_merge.py`: 22 passed.
