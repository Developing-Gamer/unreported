Draw Nominal scales like categorical axes in the objects interface

## Overview
`so.Plot` axes with a `Nominal` scale (explicit or inferred) were drawn like plain linear axes. They now follow the conventions of seaborn's categorical plots: the axis spans -0.5 to n-0.5 around the first and last tick instead of using normal margins, the grid is hidden even if the active style enables it, and a nominal y axis is inverted. Explicit `Plot.limit()` values still take precedence.

## Details
- Added a no-op `Scale._finalize(p, axis)` hook and a `Nominal._finalize` implementation in `seaborn/_core/scales.py`. It turns the grid off, then sets the limits from the number of major ticks (on the axis, so shared and faceted axes cover all categories), swapping them for y.
- `Plotter._finalize_figure` calls the hook for each subplot axis *before* applying user limits, so `.limit()` overrides the default categorical limits (including for paired axes such as `x0`).

## Verification
- New tests in `tests/_core/test_plot.py` (`test_nominal_x_axis_tweaks`, `test_nominal_y_axis_tweaks`, `test_nominal_axis_tweaks_with_grid_style`) failed before the change and pass after it.
- `pytest tests/_core tests/_marks tests/_stats`: 629 passed, 6 xfailed. flake8 is clean.
- Run with `/opt/miniconda3/envs/testbed/bin/python -m pytest tests/_core/test_plot.py -k nominal_`.
