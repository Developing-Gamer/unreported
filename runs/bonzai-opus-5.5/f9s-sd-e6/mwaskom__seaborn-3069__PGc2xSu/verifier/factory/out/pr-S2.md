Draw Nominal scales like categorical axes in the objects interface

## Overview
Classic categorical plots draw the category axis with ±0.5 padding around the first and last tick, no grid, and an inverted y axis. `so.Plot` axes with a `Nominal` scale (explicit or inferred) used matplotlib's default margins, kept the style's grid, and were not inverted on y. They now match the classic behaviour.

## Details
- `Plotter._finalize_figure` (seaborn/_core/plot.py): for each subplot axis whose scale is `Nominal`, turn the grid off. Unless the user passed `Plot.limit` for that axis, set limits to `(-.5, n - .5)` (reversed for y, which inverts it), with `auto=None`, mirroring `_adjust_cat_axis`. `n` is the number of major ticks. Explicit limits still win.
- Tests in tests/_core/test_plot.py: x and y axes (limits, grid, inversion), explicit limit override, paired axes.

## Verification
- New tests failed before the change (limits were (-0.055, 2.055)) and pass after.
- `pytest tests/_core tests/_marks tests/_stats`: 628 passed, 6 xfailed. flake8 clean on plot.py.
