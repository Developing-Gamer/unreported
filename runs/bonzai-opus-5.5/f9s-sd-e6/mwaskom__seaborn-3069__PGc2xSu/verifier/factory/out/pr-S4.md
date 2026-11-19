Fix palette widget colormaps keeping stale under/over colors

Overview: After choosing a palette in the interactive widgets (e.g. `choose_colorbrewer_palette("sequential")`), values above a fixed `vmax` in a heatmap rendered black instead of the palette's darkest color (and values below `vmin` rendered white). The widget colormap is initialised from "Greys" and its under/over entries were computed once from that.

Details: `_update_lut` overwrote only the 256 LUT entries in place. It now calls `cmap._set_extremes()` afterwards so the under/over entries follow the new palette. Added `tests/test_widgets.py`, which checks that `cmap(np.inf)`/`cmap(-np.inf)` match the ends of the chosen palette; it fails before the fix (over is `(0,0,0,1)`).

Verification: `python -m pytest tests/test_widgets.py tests/test_palettes.py` passes.
