Fix legend labels for large numeric ranges dropping the formatter offset

## Root cause
Numeric legends are labeled with matplotlib's `ScalarFormatter`. For large values, or a small range sitting on a large base, that formatter uses an offset or a scientific-notation multiplier (e.g. `1e6`, `+1e6`). Normally the multiplier is drawn separately at the axis edge, and only the reduced tick text goes into each label. Legends never show that multiplier, so the entries were wrong: values around 3e6 were labeled `3 … 6`, and values around 1e6+N were labeled `1.6 … 4.8`. This happened in two places:

- `seaborn/_core/scales.py` (`Continuous._setup`, used by `seaborn.objects`)
- `seaborn/utils.py` (`locator_to_legend_entries`, used by `scatterplot`/`relplot`/`lineplot` brief legends)

## Change
- `Continuous._setup`: before formatting legend labels, turn off offset and scientific notation on the formatter when it supports them (`set_useOffset` / `set_scientific`).
- `locator_to_legend_entries`: build the `ScalarFormatter` with `useOffset=False` and `set_scientific(False)`. The `LogFormatter` path is unchanged.

Legend entries now show the full values (e.g. `3000000 … 6000000`, `1000001.6 … 1000004.8`).

## Verification
- New tests `tests/_core/test_scales.py::TestContinuous::test_legend_no_offset` and `tests/test_utils.py::test_locator_to_legend_entries_no_offset`. Both fail before the change and pass after it.
- Reproduced the issue's scenario manually with both `so.Plot(...).add(so.Dot())` and `sns.scatterplot` before and after the change.
- `tests/_core`, `tests/_marks`, `tests/test_utils.py`, `tests/test_relational.py` and `tests/test_categorical.py` pass, except `TestCatPlot::test_share_xy`. That test also fails on the unmodified checkout because of an environment DeprecationWarning.
