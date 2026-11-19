Don't warn about numeric pass-through for empty data on a category axis

## Overview
Plotting empty data (`ax.plot([], [])`) on an axis that already has string categories raised `ConversionError: Failed to convert value(s) to axis units: array([], dtype=float64)` whenever MatplotlibDeprecationWarning was an error. `StrCategoryConverter.convert` decided that input was "numbers passed through" because `all()` over zero items is True, and emitted the 3.5 deprecation warning; `Axis.convert_units` then wrapped it in ConversionError.

## Details
- `lib/matplotlib/category.py`: return an empty float array early when the input is empty, with no warning. Empty input contains no numbers and no categories.
- `lib/matplotlib/tests/test_category.py`: `test_empty_data_no_deprecation_warning` plots empty data on a category axis with the deprecation warning set to error. It failed with the production ConversionError before the fix.

## Verification
`pytest lib/matplotlib/tests/test_category.py lib/matplotlib/tests/test_units.py`: 103 passed, 8 xfailed. flake8 clean.
