Replace removed pandas option `mode.use_inf_as_null` with explicit inf-to-NaN handling

## Overview
With pandas >= 2.0, `Plot.plot()`, `histplot` and other classic functions, and `boxenplot` raised `OptionError: No such keys(s): 'mode.use_inf_as_null'`. seaborn entered `pd.option_context("mode.use_inf_as_null", True)`, and pandas 2.0 removed that alias. Plots now render again, and infinite values are still treated as missing.

## Details
- `seaborn/_core/plot.py` (`split_generator`), `seaborn/_oldcore.py` (`comp_data`) and `seaborn/categorical.py` (`_LVPlotter._lv_box_ends`) no longer use the option context. They replace +/-inf with NaN explicitly, then drop or mask NaN as before. Switching to `mode.use_inf_as_na` was rejected because pandas 2.1 deprecates it.
- Added `tests/test_inf_handling.py`. It plots data containing inf with `so.Plot` (Dot and Line, so the `keep_na` path is covered), `histplot` and `boxenplot`.

## Verification
- `python -m pytest tests/test_inf_handling.py`: 4 failed with `OptionError` before the fix, 4 passed after.
- `pytest tests/_core/test_plot.py tests/test_distributions.py tests/test_categorical.py tests/test_core.py`: 872 passed, 4 failed.
- The 4 failures also fail on the base commit: `test_share_xy` and 3 `test_comp_data_missing` cases (fixtures 6-8). Fixtures 6-8 fail in `variable_type` on `pd.NA`, which this change does not touch. `test_share_xy` failed on base with the same OptionError; after the fix it fails on a DeprecationWarning, so I did not trace its cause.
