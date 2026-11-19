Include the data maximum in brief numeric legends

## Root cause
`seaborn.utils.locator_to_legend_entries` removes locator ticks that fall outside the data limits with `l >= limits[0] and l < limits[1]`. Because the upper bound is strict, a tick exactly at the data maximum is dropped. For example, hue values from 0–100 give legend entries 0, 20, …, 80 even though points at 100 are drawn. The existing test `test_locator_to_legend_entries` (which expects `["2", "4", "6"]` for limits `(1, 6)`) was failing because of this.

## Change
Use an inclusive upper bound: `l <= limits[1]`.

## Verification
- `tests/test_utils.py::test_locator_to_legend_entries` now passes. I added a case for limits `(0, 100)` that expects `0 … 100`; it fails before the change.
- `tests/test_utils.py` and `tests/test_relational.py` pass.
