Update over/under/bad colors when interactive palette widgets change the colormap

## Root cause
`seaborn.widgets._init_mutable_colormap` creates a "Greys" colormap and sets up its LUT, including the over, under and bad entries. When the user picks a new palette, `_update_lut` overwrites only `cmap._lut[:256]`, so the over/under entries keep the Greys values. As a result, values above `vmax` (e.g. in a heatmap with a fixed color scale) are drawn near-black instead of in the chosen palette's top color, for example red.

## Change
`_update_lut` now calls `cmap._set_extremes()` after writing the new colors, so the over/under/bad entries are derived from the updated LUT.

## Verification
New test `tests/test_widgets.py::test_update_lut_updates_extremes`: after the LUT is updated to a red ramp, `cmap(inf)` / `cmap(1.5)` equal the last red and `cmap(-inf)` / `cmap(-0.5)` equal the first. It fails before the change and passes after it.
