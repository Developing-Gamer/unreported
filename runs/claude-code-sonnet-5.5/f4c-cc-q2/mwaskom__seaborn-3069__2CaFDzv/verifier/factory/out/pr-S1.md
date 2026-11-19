Replace removed pandas option `mode.use_inf_as_null` with `mode.use_inf_as_na`

Root cause: `pd.option_context("mode.use_inf_as_null", ...)` is used in `Plotter._plot_layer.split_generator` (`seaborn/_core/plot.py`), `VectorPlotter.comp_data` (`seaborn/_oldcore.py`) and `_LVPlotter._lv_box_ends` (`seaborn/categorical.py`). pandas 2.0 removed that alias, so every `Plot.plot()` raised `OptionError: No such keys(s): 'mode.use_inf_as_null'`.

Change: use the equivalent `mode.use_inf_as_na` option in all three places.

Verification: on the pandas 2.0 / matplotlib 3.7 environment the full test suite went from 647 failures to 6; the remaining 6 fail identically without my changes (nullable-dtype `NA` ambiguity, an mpl projection message, a deprecation warning, and a log-scale mesh test). The updated suites (tests/_core, test_utils, test_distributions, test_matrix, test_relational) otherwise pass.
