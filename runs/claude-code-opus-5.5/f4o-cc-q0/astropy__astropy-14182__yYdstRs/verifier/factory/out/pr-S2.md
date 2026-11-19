TimeSeries: require the required columns to be the leading columns, in order

## Root cause
`BaseTimeSeries._check_required_columns` had been changed to test `set(required_columns).issubset(self.colnames)`. That checks only that the columns are present, not that they come first and in order. So `ts.add_column(col, index=0)` put a non-time column ahead of `time` and was accepted silently, even though the error message itself says "expected 'time' as the first column". (The existing `test_required_columns` failed with `DID NOT RAISE`.) The confusing message from the issue ("expected 'time' ... but found 'time'") is already gone: the message now lists all required columns.

## Change
Restored the ordered prefix comparison `self.colnames[: len(required_columns)] != required_columns` in `astropy/timeseries/core.py`. This keeps the improved message from #13009.

## Verification
- The existing `test_required_columns` passes again. It checks that adding a column at index 0 must raise, and it also covers the issue's `remove_column` scenario with `['time', 'a']` required.
- Added a case where both required columns are still present but another column is inserted between them. It must raise `... expected ['time', 'a'] ... but found ['time', 'b2']`.
- `pytest astropy/timeseries`: the only failures left need network or come from numpy deprecations (leap-second auto-update, BLS doctests). They fail the same way without this change.

Related: S3 (production report of CSVs gaining a field ahead of the timestamp). With this check restored, loading such data into a `TimeSeries` with a non-time first column fails right away instead of being accepted.
