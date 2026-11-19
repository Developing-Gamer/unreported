Fix ConversionError when converting empty data on a category axis

`StrCategoryConverter.convert` decided input was a "numeric pass-through" with `all(...)` over the values. For an empty array `all()` is True, so it emitted the 3.5 "numbers passed through unit converters" deprecation warning. With deprecation warnings as errors, `Axis.convert_units` wraps that into `ConversionError: Failed to convert value(s) to axis units: array([], dtype=float64)` (e.g. `ax.plot(['a','b'],[1,2]); ax.plot([],[])`).

Fix: return an empty float array from `StrCategoryConverter.convert` when there is nothing to convert, without the deprecation warning.

Test: `test_category.py::test_plot_empty_on_category_axis` fails before the fix with the ConversionError above and passes after. `test_category.py` and `test_units.py` pass (103 passed, 8 xfailed).
