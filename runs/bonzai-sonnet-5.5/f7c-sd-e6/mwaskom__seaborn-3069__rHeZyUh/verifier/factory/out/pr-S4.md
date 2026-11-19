Refresh under/over/bad colors when palette widgets update the colormap

## Overview
After choosing a palette in the interactive widgets (e.g. a red gradient with `as_cmap=True`), heatmap cells above a fixed `vmax` were drawn in the near-black end of the original Greys map instead of the end of the chosen gradient. The same stale colour affected values below `vmin`.

## Details
The widgets build one mutable colormap from Greys and `_update_lut` overwrote only `_lut[:256]`. Matplotlib stores the under/over/bad colours in extra entries after those 256, which `_set_extremes()` filled once from the Greys ends at creation. `_update_lut` now calls `cmap._set_extremes()` after writing the new colours so those entries follow the palette.

Added `tests/test_widgets.py`, which checks that `cmap(np.inf)` and `cmap(-np.inf)` match the last and first palette colours after `_update_lut`. It failed before the fix (over colour was black, expected red).

## Verification
`pytest tests/test_widgets.py tests/test_matrix.py tests/test_miscplot.py` passes.
