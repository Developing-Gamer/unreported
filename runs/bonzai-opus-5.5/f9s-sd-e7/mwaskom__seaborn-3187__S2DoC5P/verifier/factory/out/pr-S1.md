Fix legend labels for large numeric ranges losing their multiplicative offset

## Overview
Numeric legends (both `seaborn.objects` and `scatterplot`/`lineplot` with `hue`/`size`) formatted their entries with a default `ScalarFormatter`. For large values (e.g. 3e6–6e6) it moves a shared exponent/offset out of each label into a separate offset string that seaborn never draws, so legend entries read `3, 4, 5, 6` instead of `3000000, ...`. Reported as a wrong-legend issue in v0.12.1.

## Details
- `ContinuousBase._setup` (`seaborn/_core/scales.py`): when the legend formatter is a `ScalarFormatter`, call `set_useOffset(False)` and `set_scientific(False)` before `format_ticks`. Only the legend path is affected, not axis tick labels.
- `utils.locator_to_legend_entries` (`seaborn/utils.py`): same for the `ScalarFormatter` used for brief legends.
- Regression tests: `tests/_core/test_scales.py::TestContinuous::test_legend_large_values`, `tests/test_utils.py::test_locator_to_legend_entries_large_values` (limits (1000001, 1000005) and (2.7e6, 6.3e6)).
- whatsnew entry in v0.12.2.

## Verification
- `python -m pytest tests/_core/test_scales.py tests/test_utils.py -q -k large_values`: 3 fail before the fix (labels `3.0, 4.5, 6.0` vs levels 3000000...), pass after.
- Full `tests/_core/test_scales.py tests/test_utils.py`: only `test_tick_minor` and the two `test_move_legend_*` fail, identically on the base commit (environment's matplotlib/pandas versions).
