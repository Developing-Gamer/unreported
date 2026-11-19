Fix legend labels for large numeric ranges losing their offset

## Overview
Legends for continuous properties (e.g. `pointsize="body_mass_mg"`, values 3e6–6e6) showed labels such as `3`, `4`, `5`. The axis `ScalarFormatter` had switched on an offset/scientific notation and returned only the mantissas; the `1e6` multiplier lives in a separate offset text, which a legend can't show. Legend entries were therefore wrong by a factor of 10^n.

## Details
In `ContinuousBase._setup` (`seaborn/_core/scales.py`), when building `_legend`, the major formatter now has `set_useOffset(False)` and `set_scientific(False)` called (when supported) before `format_ticks`, so labels carry the full values. Axis tick labels are unaffected, since this is only done in the legend branch.

Test: `tests/_core/test_scales.py::TestContinuous::test_legend_large_values_no_offset`.

## Verification
- `python -m pytest tests/_core/test_scales.py -k legend_large -q`: failed before (`assert 3.0 == 3000000.0`), passes after.
- `tests/_core` and `tests/test_utils.py`: 554 passed; one failure, `tests/_core/test_moves.py::TestDodge::test_gap`, fails identically on the base commit and is unrelated.
