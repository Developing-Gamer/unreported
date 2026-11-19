Fix ConversionError when plotting empty data on a categorical axis

## Overview
Plotting empty data (`ax.plot([], [])`) on an axis that already has string categories issued the 3.5 "passing numbers through unit converters is deprecated" warning. Where warnings are errors, `Axis.convert_units` wrapped it as `ConversionError: Failed to convert value(s) to axis units: array([], dtype=float64)` (553 Sentry events, 35 users in 7 days).

## Details
- Cause: `units._is_natively_supported` returns None for an empty iterable, so empty data reaches `StrCategoryConverter.convert`. There `all(...)` over zero values is vacuously true, so empty input was treated as "numbers passed through" and triggered the deprecation warning.
- Fix: in `lib/matplotlib/category.py`, only take the numbers path when `values.size` is non-zero. Empty input falls through to the normal mapping, which returns an empty float array (`otypes=[float]`).
- Tests (`lib/matplotlib/tests/test_category.py`): `test_convert_empty_array` and `test_plot_empty_after_categories`, both with warnings as errors. Both failed with the ConversionError before the fix.
- No overlap with open PRs #1000 / #1001 (AFM, Bezier).

## Verification
`python -m pytest lib/matplotlib/tests/test_category.py lib/matplotlib/tests/test_units.py -q`: 104 passed, 8 xfailed. The two new tests fail before the fix and pass after.
