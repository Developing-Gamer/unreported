Don't emit the numeric-passthrough deprecation for empty data in StrCategoryConverter

Fixes S8, and S7 (the production Sentry `ConversionError: ... array([], dtype=float64)` raised from `category.py` `convert` -> `warn_deprecated`), which has the same root cause.

## Root cause

`Axis.convert_units` returns early only for data that `units._is_natively_supported` recognizes as numeric. For an empty iterable that check returns `None` (falsy), so empty data still goes to the axis converter. In `StrCategoryConverter.convert`, the test

```python
is_numlike = all(... for v in values)
```

is vacuously `True` for an empty array. Empty input therefore went down the deprecated "pass numbers through unit converters" branch and raised a `MatplotlibDeprecationWarning`. When warnings are turned into errors, as in the Sentry event and the issue traceback, that warning surfaces as `ConversionError`. Both `ax.plot([], [])` and the suggested workaround `ax.convert_xunits([])` hit it.

## Change

`lib/matplotlib/category.py`: only take the deprecated numeric-passthrough branch when the input is non-empty (`if values.size and is_numlike:`). Empty input now takes the normal path: `unit.update` on an empty array does nothing, and the vectorized mapping returns an empty float array. Behaviour for non-empty numeric input, including the deprecation warning, is unchanged.

## Verification

- Added `test_no_deprecation_on_empty_data` to `lib/matplotlib/tests/test_category.py`. It turns `MatplotlibDeprecationWarning` into an error and checks that `ax.plot([], [])` and `ax.convert_xunits([])` on a categorical axis succeed and return empty data.
- The test fails without the fix and passes with it.
- `pytest lib/matplotlib/tests/test_category.py lib/matplotlib/tests/test_units.py lib/matplotlib/tests/test_dates.py`: 192 passed, 8 xfailed.
