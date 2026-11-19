Fix ConversionError when plotting empty data on a categorical axis

**Problem:** On an axis with category units, `ax.plot([], [])` (empty data) raised `ConversionError: Failed to convert value(s) to axis units: array([], dtype=float64)` when warnings are errors. `StrCategoryConverter.convert` decided the input was "numbers passed through the converter" using `all(...)` over the values, which is vacuously true for an empty array. It then emitted the 3.5 deprecation warning, which `Axis.convert_units` wrapped as `ConversionError`.

**Fix:** `StrCategoryConverter.convert` only takes the deprecated numeric pass-through path when there are values (`values.size and is_numlike`). Empty input goes through the normal mapping and returns an empty float array.

**Tests:** added `test_convert_empty_array` and `test_plot_empty_with_categories` in `lib/matplotlib/tests/test_category.py`; both failed before the fix with the production error and pass now.

Verification: `python -m pytest lib/matplotlib/tests/test_category.py lib/matplotlib/tests/test_units.py` -> 104 passed, 8 xfailed.
