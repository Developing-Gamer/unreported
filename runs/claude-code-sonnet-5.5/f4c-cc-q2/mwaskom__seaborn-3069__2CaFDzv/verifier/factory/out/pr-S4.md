Update over/under/bad colors when the palette widgets change the colormap

Root cause: `seaborn.widgets._update_lut` wrote only the first 256 LUT entries. Matplotlib stores the under/over/bad colors in `_lut[N:N+3]`, so they kept the initial Greys values (almost black for "over"). The assignment also broadcast an (256, 3) RGB array into the (256, 4) RGBA LUT, which raises with the installed matplotlib.

Change: `_update_lut` converts colors with `to_rgba_array` and calls `cmap._set_extremes()` after updating the LUT.

Verification: new test `test_interactive_cmap_extremes_follow_lut` in tests/test_matrix.py fails before and passes after.
