Keep a tick equal to the data maximum in brief numeric legends

## Overview
On some scatter plots the brief hue/size legend stopped short of the data maximum: with values 0–100 the legend ended at 80 although points at 100 were drawn. The legend now includes a tick that falls exactly on the maximum.

## Details
`utils.locator_to_legend_entries` clipped locator ticks with `l >= limits[0] and l < limits[1]`, so a tick equal to the upper limit was dropped. This only shows when the maximum is a "nice" tick (e.g. `MaxNLocator(nbins=6)` on (0, 100) gives 0, 20, ..., 100), hence "a few reports". The filter is now inclusive (`<=`). Both hue and size legends in `relational.py` use this function, so both are fixed. The existing `test_locator_to_legend_entries` (limits (1, 6) -> `["2", "4", "6"]`) already expected this and was failing.

Tests added: `test_locator_to_legend_entries_includes_max_tick` (tests/test_utils.py) and `TestScatterPlotter.test_brief_legend_includes_max_tick` for hue and size (tests/test_relational.py).

## Verification
- Before the fix: `test_locator_to_legend_entries`, the new utils test and both new scatter tests fail (`['2','4'] != ['2','4','6']`, last label not `'100'`).
- After: `pytest tests/test_utils.py tests/test_relational.py` -> 122 passed.
