Fix pseudonetcdf backend ignoring decode_timedelta

## Overview
Forecast lead-time columns stored with units such as `hours` came back as `timedelta64` durations instead of plain 6 and 12, even with `decode_timedelta=False`. `PseudoNetCDFBackendEntrypoint.open_dataset` passed `decode_times` to the store entrypoint where `decode_timedelta` belongs, so the user's flag was discarded. It now forwards `decode_timedelta`. Datetime variables ("hours since ...") are unaffected.

## Details
- `xarray/backends/pseudonetcdf_.py`: `decode_timedelta=decode_times` -> `decode_timedelta=decode_timedelta`. When it is `None`, `decode_cf_variables` still falls back to `decode_times`, so the default is unchanged.
- `xarray/tests/test_backends.py`: new `TestPseudoNetCDFFormat.test_decode_timedelta_false` calls xarray's own `PseudoNetCDFBackendEntrypoint` directly (recent PseudoNetCDF releases register their own plugin under the same engine name, which would shadow it). Variable with `units="hours"`: int with `decode_timedelta=False`, `timedelta64[ns]` by default.
- `doc/whats-new.rst`: bug-fix entry.

## Verification
- Before the fix the new test fails: `AssertionError: assert 'm' == 'i'` (dtype kind timedelta instead of int).
- After: `python -m pytest xarray/tests/test_backends.py -k TestPseudoNetCDFFormat` -> 4 passed, 1 skipped, 1 xfailed.
- Note: the local env needed a tiny shim for a pandas import in test_dataset.py (unrelated, pre-existing); PseudoNetCDF was pip-installed for the test.
