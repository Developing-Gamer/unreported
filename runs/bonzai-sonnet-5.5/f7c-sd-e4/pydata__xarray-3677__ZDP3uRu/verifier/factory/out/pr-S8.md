Raise RuntimeError instead of caching None when an accessor's __init__ raises AttributeError

## Overview
A custom accessor (e.g. a calibration helper registered on Dataset) whose `__init__` hit a missing attribute came back as `None`, with no error or log line. Because the `None` was cached on the object, every later access on the same dataset also returned `None`.

## Cause
`_CachedAccessor.__get__` caught `AttributeError` from the accessor constructor, set the accessor to `None` and stored that in `obj._cache`.

## Fix
`__get__` now raises `RuntimeError("error initializing 'name' accessor.")` chained from the original error (GH933), and nothing is cached on failure, so a later attempt can succeed. The existing regression test `test_broken_accessor` already expects this.

## Verification
`python -m pytest xarray/tests/test_extensions.py -q`: before the fix `test_broken_accessor` fails (no RuntimeError raised); after the fix, 4 passed.
