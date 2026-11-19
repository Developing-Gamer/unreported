Draw Nominal scales like categorical axes in the objects interface

Root cause: `Plotter._finalize_figure` applied no special handling to axes with a `Nominal` scale, so they got the usual margins, a style grid, and a non-inverted y axis, unlike the function-interface categorical plots.

Change: in `_finalize_figure`, for each axis with a `Nominal` scale, turn the grid off, and, unless the user set explicit limits, set the limits to -.5 .. n-.5 (reversed on y). `Nominal` is now imported at module level in `plot.py`. Added a whatsnew entry.

Verification: new tests `test_nominal_axis_drawn_like_categorical[x|y]` (grid enabled via rc, checks limits and hidden grid) and `test_nominal_axis_respects_explicit_limits`; they fail before the change and pass after.
