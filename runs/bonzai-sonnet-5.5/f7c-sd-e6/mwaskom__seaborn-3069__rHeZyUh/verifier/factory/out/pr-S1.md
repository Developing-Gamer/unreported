Stop using the removed pandas option `mode.use_inf_as_null`

## Overview
On pandas >= 2.0 every `so.Plot(...).plot()` raised `OptionError: "No such keys(s): 'mode.use_inf_as_null'"`, because `Plot` wrapped its NaN handling in `pd.option_context('mode.use_inf_as_null', True)`. pandas removed that option in 2.0. The same call sat in the classic `comp_data` (relational, distribution and categorical plots) and in `_LVPlotter._lv_box_ends` (boxenplot). Infinite values are now converted to NaN explicitly, so the code no longer depends on any pandas option.

## Evidence
Sentry: 447 events, 56 users in 7 days. Stack: `seaborn/_core/plot.py` `_plot_layer` -> `split_generator` -> `pandas/_config/config.py __enter__`.

## Details
- `seaborn/_core/plot.py` (`split_generator`): `axes_df.replace([np.inf, -np.inf], np.nan)` before the existing `keep_na`/`dropna` handling. Added the missing `numpy` import.
- `seaborn/_oldcore.py` (`comp_data`): `orig.replace([np.inf, -np.inf], np.nan).dropna()`.
- `seaborn/categorical.py` (`_lv_box_ends`): infinities are replaced by NaN and dropped through a `pd.Series`, which still copes with object arrays from nullable dtypes.
- I did not switch to `mode.use_inf_as_na`: it is deprecated in pandas 2.1 and removed in 3.0.
- Not changed: the pandas pin and CI matrix, and the release note suggested in the investigation. The fix does not need them.
- Test added: `tests/_core/test_plot.py::TestPlotting::test_infinite_values_dropped`.

## Verification
- Before the fix, `pytest tests/_core/test_plot.py -k infinite_values` fails with `OptionError: "No such keys(s): 'mode.use_inf_as_null'"`. After the fix it passes.
- Ran `tests/test_relational.py tests/test_core.py tests/test_categorical.py tests/_core` on pandas 2.0.0 / numpy 1.25.2. 1025 passed, 4 failed. The 4 failures are not caused by this change:
  - 3 are `test_comp_data_missing[...pd.NA...]`. They fail in `variable_type` on `pd.NA`, and also fail on the base commit, which has 6 failures in that test.
  - `TestCatPlot::test_share_xy` fails on base with the OptionError. With this change it still fails, now on a numpy 1.25 `np.find_common_type` DeprecationWarning that the test run turns into an error.
- I did not complete the full test suite, which takes more than 10 minutes here.
