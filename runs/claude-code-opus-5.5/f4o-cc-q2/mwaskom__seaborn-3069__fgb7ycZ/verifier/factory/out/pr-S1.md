Fix OptionError for 'mode.use_inf_as_null' with pandas >= 2.0

## Root cause
Three places in seaborn wrapped missing-data filtering in
`pd.option_context("mode.use_inf_as_null", True)` so that `±inf` was treated as missing:

- `seaborn/_core/plot.py` (`Plotter._setup_split_generator.split_generator`), used by every `Plot.plot()` call that draws a layer
- `seaborn/_oldcore.py` (`VectorPlotter.comp_data`)
- `seaborn/categorical.py` (`_LVPlotter._lv_box_ends`, used by boxenplot)

pandas 2.0 removed that option, so entering the context raises
`OptionError: "No such keys(s): 'mode.use_inf_as_null'"`. The production trace comes from the first of these.

## Change
Removed the option context and handle infinities directly:
- `plot.py`: work out which rows have no null values, then among those rows mark any with `±inf` as not present. These rows are dropped, or in `keep_na` mode their x/y are set to NaN, as before. The inf check only runs on non-null rows because `isin` can fail on `pd.NA`.
- `_oldcore.py`: `orig.dropna()` followed by removing `±inf`.
- `categorical.py`: drop nulls, then drop `±inf` with `np.isin`. This works for object arrays that come from nullable `Float64` input.

This works on every pandas version, and avoids the replacement option `use_inf_as_na`, which is itself deprecated in pandas 2.1.

## Verification
- New `TestPlotting::test_split_drops_infinite_values` (tests/_core/test_plot.py) and `TestBoxenPlotter::test_box_ends_drop_missing_and_infinite` (tests/test_categorical.py). Both fail before the change with this OptionError and pass after it.
- Three `TestVectorPlotter::test_comp_data_missing` cases that failed with the OptionError now pass. Cases 6–8 still fail for an unrelated reason that was already there: `np.isin` on `pd.NA` in `variable_type`.
- `tests/_core`, `tests/test_core.py`, `tests/test_categorical.py` and `tests/test_utils.py` pass, apart from failures that also happen on the untouched code (numpy 1.25 / matplotlib 3.7 deprecation issues).
