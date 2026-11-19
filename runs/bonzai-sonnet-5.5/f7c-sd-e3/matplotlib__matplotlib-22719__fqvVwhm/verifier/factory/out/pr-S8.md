Don't warn about numeric pass-through for empty data on a category axis

No pull request opened: open PR #1002 already fixes this issue, so nothing was changed.

## Cause
`StrCategoryConverter.convert` (lib/matplotlib/category.py) decides whether the input is already numeric with `all(is_numlike(v) ... for v in values)`. For empty data, `all([])` is True, so `ax.xaxis.update_units(["a", "b"]); ax.plot([], [])` emitted "Support for passing numbers through unit converters is deprecated" although no numbers were passed.

## Fix (already in PR #1002)
Return an empty float array early when `values.size == 0`, before the numeric pass-through and its warning. A test plots empty data on a category axis with MatplotlibDeprecationWarning turned into an error.

## Verification
Not run: pytest is not installed in this environment.
