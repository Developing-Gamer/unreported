Fix numeric legends dropping the formatter offset for large values

## Overview
Numeric legend entries for large values (e.g. `pointsize` of 2.7e6–6.3e6) were shown as `3`, `4`, `5`, `6` because matplotlib's `ScalarFormatter` moved the shared multiplier/offset out of the labels, and seaborn never draws that offset text. Legends now show the full values.

## Evidence
GitHub issue: "Wrong legend values of large ranges" (since 0.12.1). `so.Plot(..., pointsize="body_mass_mg").add(so.Dot())` showed legend labels without the 1e6 multiplier. The classic `scatterplot`/`lineplot` brief legends go through `utils.locator_to_legend_entries`, which has the same defect.

## Details
- `seaborn/_core/scales.py`: in `ContinuousBase._setup`, before formatting legend labels, disable offset and scientific notation on the formatter (when it supports it). Only the legend labels are affected; this uses a private pseudo-axis.
- `seaborn/utils.py`: `locator_to_legend_entries` does the same for its `ScalarFormatter`.
- Tests: `tests/_core/test_scales.py::TestContinuous::test_legend_large_values_no_offset` and `tests/test_utils.py::test_locator_to_legend_entries_large_values`; both fail before the fix (labels `['1', '3', '4']` instead of `['1000001', ...]`) and pass after.
- Whatsnew entry in `doc/whatsnew/v0.12.2.rst`.

## Verification
`pytest tests/_core tests/test_utils.py tests/test_relational.py`: 631 passed, 1 failed (`tests/_core/test_moves.py::TestDodge::test_gap`), which fails identically on the base commit and is unrelated.
