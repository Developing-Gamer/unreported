Include the data maximum in brief numeric legends

## Overview
On scatter (and line) plots with `legend="brief"`, the hue/size legend stopped one step early when the data maximum landed on a tick: data 0..100 gave a legend ending at 80, although the 100 points are drawn. The legend now includes the tick equal to the maximum.

## Details
`locator_to_legend_entries` in `seaborn/utils.py` clipped locator ticks to the data range with `l >= limits[0] and l < limits[1]`. The strict upper bound dropped a tick equal to the data max. It is now `l <= limits[1]`, symmetric with the lower bound. `limits` come from the min/max of the data levels (`relational.py` hue/size brief legends), so the max is always an observed value.

## Reproduction / tests
- `tests/test_utils.py::test_locator_to_legend_entries` already expected `['2','4','6']` for limits (1, 6) and failed before (`['2','4']`).
- New `tests/test_relational.py::TestScatterPlotter::test_brief_legend_includes_max_tick`: hue = 0,10,...,100 expects the last legend text to be `100`; failed before (`80`).

## Verification
- Both tests fail on the base commit and pass with the fix.
- `pytest tests/test_utils.py tests/test_relational.py` passes. `tests/test_core.py::...test_comp_data_missing` fails independently of this change (`TypeError: boolean value of NA is ambiguous`, a pandas NA issue unrelated to legends).
