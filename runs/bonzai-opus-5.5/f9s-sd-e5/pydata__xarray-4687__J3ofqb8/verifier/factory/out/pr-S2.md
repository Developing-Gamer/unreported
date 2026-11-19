Fix default backend priority: prefer netcdf4 over h5netcdf

## Overview
Ingestion runs started recording `h5netcdf` as the reader for inputs that previously used `netcdf4`, even though both libraries are installed. `sort_backends` iterated `sorted(STANDARD_BACKENDS_ORDER)`, which turned the intended priority `[netcdf4, h5netcdf, scipy]` into alphabetical `[h5netcdf, netcdf4, scipy]`. `guess_engine` returns the first engine that can open the file, so `.nc` files opened with h5netcdf. They now open with netcdf4 again.

## Evidence
Message in `data-ingestion-support` (production): recent runs record h5netcdf in reader metadata where the same inputs previously recorded netcdf4; both readers installed, jobs finish normally.

## Details
- `xarray/backends/plugins.py`: iterate `STANDARD_BACKENDS_ORDER` directly instead of its sorted copy. Non-standard backends are still appended alphabetically.
- `xarray/tests/test_plugins.py`: new `test_sort_backends_standard_priority` asserts `sort_backends` returns `[netcdf4, h5netcdf, scipy, zarr]`. The existing `test_build_engines_sorted` also failed before the fix.
- `doc/whats-new.rst`: bug-fix entry.

## Verification
- Before: `python -m pytest xarray/tests/test_plugins.py` gave 2 failed (`test_build_engines_sorted`, and the new test with `At index 0 diff: 'h5netcdf' != 'netcdf4'`).
- After: 11 passed; `plugins.guess_engine('file.nc')` returns `netcdf4`.
