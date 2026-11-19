Respect STANDARD_BACKENDS_ORDER when sorting backends (netcdf4 before h5netcdf)

## Overview
Ingestion runs that call `open_dataset` without an engine started recording `h5netcdf` where they previously recorded `netcdf4`. `sort_backends` iterated `sorted(STANDARD_BACKENDS_ORDER)`, which turned the intended priority `[netcdf4, h5netcdf, scipy]` into alphabetical `[h5netcdf, netcdf4, scipy]`. `guess_engine` returns the first backend whose `guess_can_open` matches, and both netcdf4 and h5netcdf accept HDF5 files, so h5netcdf won. Files still opened fine, so jobs finished.

## Details
- `xarray/backends/plugins.py`: iterate `STANDARD_BACKENDS_ORDER` directly.
- `xarray/tests/test_plugins.py`: add `test_sort_backends_standard_order`, which asserts the exact order netcdf4, h5netcdf, scipy, then other backends alphabetically. The existing `test_build_engines_sorted` would pass with the wrong order.

## Verification
- Before the fix the new test fails: `At index 0 diff: 'h5netcdf' != 'netcdf4'`.
- After the fix `pytest xarray/tests/test_plugins.py` passes (11 passed).
- `list(xr.backends.list_engines())` now starts `['netcdf4', 'h5netcdf', 'scipy', ...]`.
