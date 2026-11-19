Stop using the removed pandas option `mode.use_inf_as_null`

## Overview
With pandas >= 2.0, `Plot.plot()`/`show()` raises `OptionError: No such keys(s): 'mode.use_inf_as_null'` (Sentry: 447 events, 56 users in 7 days). Seaborn wrapped its NaN handling in `pd.option_context('mode.use_inf_as_null', True)`, an option pandas deprecated and then removed in 2.0. This change treats infinite values as missing explicitly, without any pandas option, so plots work again and infinite values are still dropped.

## Details
- `seaborn/_core/plot.py` (`split_generator`): `axes_df.replace([np.inf, -np.inf], np.nan)` before the existing `keep_na`/`dropna` logic; added the missing `numpy` import.
- `seaborn/_oldcore.py` (`comp_data`): same replacement on `orig` before `dropna()`; fixes the classic relational/distribution/categorical plots.
- `seaborn/categorical.py` (`_lv_box_ends`): drop nulls, then drop non-finite values with `np.isfinite`; fixes `boxenplot`.
- I did not switch to `mode.use_inf_as_na`: it is deprecated in pandas 2.1 and removed in 3.0.

Tests added (each fails on the base commit with the `OptionError` above and passes now):
- `tests/_core/test_plot.py::TestPlotting::test_inf_values_are_dropped`
- `tests/test_core.py::TestVectorPlotter::test_comp_data_inf`
- `tests/test_categorical.py::TestBoxenPlotter::test_lv_box_ends_inf`

## Verification
`pytest tests/_core tests/test_core.py tests/test_categorical.py tests/test_relational.py tests/test_distributions.py` on pandas 2.0.0 / numpy 1.25.2: all pass except 4 failures unrelated to this change. Three are `test_comp_data_missing` cases with `pd.NA`, which fail in `variable_type` (`np.isin` on `pd.NA`) before reaching the changed code. The fourth is `TestCatPlot::test_share_xy`, a numpy `find_common_type` DeprecationWarning.
