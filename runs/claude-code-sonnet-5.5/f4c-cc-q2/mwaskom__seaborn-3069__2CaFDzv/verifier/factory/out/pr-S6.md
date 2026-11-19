Include the upper limit in brief numeric legend entries

Root cause: `utils.locator_to_legend_entries` filtered locator ticks with `l < limits[1]`, dropping a tick that equals the data maximum. With data from 0 to 100 and ticks at 0, 20, ..., 100, the legend stopped at 80.

Change: use `<=` for the upper bound. Added a whatsnew entry.

Verification: new test `test_locator_to_legend_entries_includes_upper_limit` in tests/test_utils.py fails before and passes after; the existing `test_locator_to_legend_entries` and relational tests still pass.
