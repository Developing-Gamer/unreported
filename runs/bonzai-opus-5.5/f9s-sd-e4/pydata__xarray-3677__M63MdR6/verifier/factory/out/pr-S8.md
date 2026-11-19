Raise RuntimeError instead of caching None when a registered accessor fails to build

## Overview
If a registered accessor's `__init__` raised `AttributeError` (e.g. a missing attribute on an incoming dataset), `_CachedAccessor.__get__` swallowed it, returned `None` and stored that `None` in the object's `_cache`. Users saw `ds.calibration` as `None` with no error, and later accesses on the same dataset kept returning `None` even after the data was fixed.

## Details
- `xarray/core/extensions.py`: the `AttributeError` is now re-raised as `RuntimeError("error initializing '<name>' accessor.")` (chained from the original). Nothing is cached on failure; only successfully built accessors are cached.
- `xarray/tests/test_extensions.py`: the existing GH933 test `test_broken_accessor` was failing on the base commit and now passes; added `test_failed_accessor_not_cached` (fail, fix data, access again builds the accessor).
- `doc/whats-new.rst`: bug-fix entry.

## Verification
`python -m pytest xarray/tests/test_extensions.py` -> 5 passed (before: `test_broken_accessor` failed, "DID NOT RAISE").
