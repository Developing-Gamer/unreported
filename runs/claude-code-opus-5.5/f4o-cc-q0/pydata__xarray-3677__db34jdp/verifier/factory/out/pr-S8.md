Raise instead of caching `None` when an accessor fails to initialize

Root cause
----------
`_CachedAccessor.__get__` (xarray/core/extensions.py) caught `AttributeError` raised while
constructing a registered accessor, set `accessor_obj = None`, and stored that in the object's
`_cache`. The user-defined helper (e.g. a `ds.calibration` accessor) therefore silently returned
`None`, with no error logged, and every later access on the same Dataset also returned the cached
`None`. That matches the report. The `AttributeError` must be re-raised as a different exception
type, because Dataset/DataArray `__getattr__` would otherwise swallow it (GH933).

Change
------
Re-raise as `RuntimeError("error initializing %r accessor.")` and do not cache anything on
failure.

Verification
------------
- The existing `TestAccessor.test_broken_accessor` (expects RuntimeError) failed on the base
  commit and now passes. It is extended to check that repeated access on the same object raises
  each time instead of returning a cached `None`.
- No new failures in the broader test run.
