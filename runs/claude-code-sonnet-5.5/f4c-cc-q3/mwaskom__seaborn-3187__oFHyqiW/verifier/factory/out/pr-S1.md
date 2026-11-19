Fix legend labels dropping ScalarFormatter offset / scientific multiplier

Root cause: Continuous scales built legend labels with `axis.major.formatter.format_ticks(locs)`, and `locator_to_legend_entries` (used by scatterplot/lineplot brief legends) called `ScalarFormatter` directly. For large ranges the formatter factors out an offset or power-of-ten multiplier, which is normally drawn on the axis but has no place in a legend, so labels showed e.g. 3.5 instead of 3,500,000 (reported in S1).

Change: disable `useOffset` and `scientific` on the formatter before formatting legend labels in `seaborn/_core/scales.py` (guarded with `hasattr` for non-ScalarFormatters) and in `seaborn/utils.py`.

Verification: added `test_legend_no_offset` and `test_legend_no_scientific` (tests/_core/test_scales.py) and `test_locator_to_legend_entries_no_offset` (tests/test_utils.py); they fail without the fix and pass with it. tests/_core, tests/test_utils.py and tests/test_relational.py pass.
