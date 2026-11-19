Fix OptionError from removed pandas option 'mode.use_inf_as_null'

## Overview
With pandas >= 2.0, `Plot.plot()` (objects interface), classic-API plots going through `VectorPlotter.comp_data` (e.g. `histplot`), and `boxenplot` raised `pandas._config.config.OptionError: "No such keys(s): 'mode.use_inf_as_null'"` (447 Sentry events, 56 users in 7 days). seaborn entered `pd.option_context("mode.use_inf_as_null", True)` to treat infinite values as missing; pandas 2.0 removed that alias.

## Details
- Rather than renaming to `mode.use_inf_as_na` (itself deprecated in pandas 2.1), the three call sites now replace `+/-inf` with `NaN` explicitly before `dropna` / `isnull`, which keeps the same semantics without a global option:
  - `seaborn/_core/plot.py` (`split_generator`, the Sentry frame); added `import numpy as np`
  - `seaborn/_oldcore.py` (`comp_data`)
  - `seaborn/categorical.py` (`_lv_box_ends`)
- Tests added: `TestPlotting::test_infinite_values_dropped` (tests/_core/test_plot.py) and `TestBoxenPlotter::test_infinite_values` (tests/test_categorical.py). The existing `test_comp_data_missing` (numeric/datetime with inf) covers `_oldcore`.

## Proof
Before (base, pandas 2.0.0): `pytest tests/_core/test_plot.py -k infinite_values_dropped` fails with `OptionError: "No such keys(s): 'mode.use_inf_as_null'"`; after: passes.

## Verification
`pytest tests/test_distributions.py tests/test_categorical.py tests/test_core.py tests/_core`: 1205 passed. Remaining 4 failures are unrelated to this change and fail on base as well:
- `test_comp_data_missing[...6-8]` (pd.NA in `variable_type`'s `np.isin`)
- `TestCatPlot::test_share_xy` (numpy `np.find_common_type` DeprecationWarning; on base it failed earlier with this same OptionError)
