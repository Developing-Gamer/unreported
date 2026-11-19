Prefer netcdf4 over h5netcdf when guessing the backend engine

Root cause: `xarray.backends.plugins.sort_backends` iterated over `sorted(STANDARD_BACKENDS_ORDER)`, i.e. alphabetically (h5netcdf, netcdf4, scipy), instead of the intended priority order (netcdf4, h5netcdf, scipy). When both readers are installed, `guess_engine` therefore picked h5netcdf for inputs that previously used netcdf4 (S2).

Change: iterate over `STANDARD_BACKENDS_ORDER` directly. Added `test_sort_backends_standard_order`, which fails without the fix.

Verification: `pytest xarray/tests/test_plugins.py xarray/tests/test_computation.py` passes (259 passed, 1 skipped).
