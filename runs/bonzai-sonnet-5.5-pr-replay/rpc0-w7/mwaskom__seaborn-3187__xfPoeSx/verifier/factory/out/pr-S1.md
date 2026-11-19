Fix wrong legend values for large ranges in the objects interface

## Overview
Legends for continuous properties over large numbers (e.g. `pointsize="body_mass_mg"`, values 3,000,000–6,000,000) showed truncated labels like `3`, `4`, `5`, because the default `ScalarFormatter` moved the `1e6` multiplier into an offset text that a legend cannot display. Legend labels are now formatted in full.

## Details
- `Continuous._setup` (`seaborn/_core/scales.py`): when building the legend, turn off `useOffset` and scientific notation on the major formatter (if it supports them) before calling `format_ticks`. Axis tick labels are unaffected, since the axis can display the offset.
- Test: `tests/_core/test_scales.py::TestContinuous::test_legend_no_offset` checks that each legend label parses back to its location value for data scaled by 1e6.
- `utils.locator_to_legend_entries` (classic API) was not changed; the report concerns the objects interface.

## Verification
- `pytest tests/_core/test_scales.py -k legend_no_offset`: fails before (`assert 2.0 == 2000000.0`), passes after.
- `pytest tests/_core/test_scales.py tests/_core/test_plot.py tests/test_utils.py`: 302 passed, 6 xfailed.
