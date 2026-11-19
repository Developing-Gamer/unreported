Don't treat empty data as numeric pass-through in StrCategoryConverter

Root cause: `StrCategoryConverter.convert` computes `is_numlike = all(... for v in values)`. For an empty input, `all([])` is `True`, so empty data on an axis with category units took the deprecated "numbers through unit converters" branch. That emitted a confusing MatplotlibDeprecationWarning, and when warnings are errors (as in the Sentry event) `Axis.convert_units` wrapped it into `ConversionError`, so `ax.plot([], [])` failed. The warning's own advice (`convert_units`) failed too. Fixes S7 and S8 (same root cause).

Change: in `lib/matplotlib/category.py`, only take the numlike branch when `values.size` is non-zero. Empty input now falls through to the normal categorical path and returns an empty float array.

Verification: added `test_empty_data_with_category_units` in `lib/matplotlib/tests/test_category.py` (plots empty data on a category axis; the suite escalates warnings to errors). It fails without the fix and passes with it; the whole `test_category.py` passes.
