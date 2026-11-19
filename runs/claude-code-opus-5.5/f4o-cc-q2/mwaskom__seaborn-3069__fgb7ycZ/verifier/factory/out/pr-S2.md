Draw Nominal scales in Plot like categorical axes (tight limits, no grid, inverted y)

## Root cause
seaborn's categorical plots draw a categorical axis in a particular way: limits at ±0.5 around the first and last tick, no grid, and an inverted y axis. `so.Plot` did none of this for `Nominal` scales, including inferred ones. Those axes got the normal margins and the theme's grid, so the objects interface was inconsistent with the rest of the library.

## Change
In `Plotter._finalize_figure` (seaborn/_core/plot.py), for each subplot axis whose scale is `Nominal`:
- turn the grid off for that axis (`axis.grid(False, which="both")`);
- if the user has not set limits with `Plot.limit`, set limits to `(-0.5, n_ticks - 0.5)`. On the y axis the limits are reversed (`(n - 0.5, -0.5)`), which inverts the axis.

Limits set with `Plot.limit` still take precedence. Setting the limits directly with `auto=None` avoids the invisible sticky-edge-artist workaround mentioned in the issue.

## Verification
- New tests `TestPlotting::test_nominal_x_axis_tweaks` and `test_nominal_y_axis_tweaks` (tests/_core/test_plot.py). They check the limits, that the grid is hidden, the y inversion, and that `Plot.limit` overrides the default limits. Both fail before the change and pass after it.
- The whole `tests/_core` suite passes.
