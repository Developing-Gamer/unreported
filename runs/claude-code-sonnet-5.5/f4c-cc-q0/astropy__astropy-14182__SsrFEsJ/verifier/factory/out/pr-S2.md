TimeSeries: enforce required column order in `_check_required_columns`

## Root cause
The check used `set(required_columns).issubset(self.colnames)`, which ignores order and position. Adding a column in front of `time` was not caught (`test_required_columns` failed with "DID NOT RAISE"), and the error path produced a confusing "found" message.

## Change
Compare the ordered prefix instead: `self.colnames[:len(required_columns)] != required_columns`. Removing a required column such as `flux` now raises "expected ['time', 'flux'] as the first columns but found 'time'". Changelog entry added.

## Verification
`astropy/timeseries/tests/test_sampled.py::test_required_columns` (which includes the #13009 case) failed before and passes now. No new failures in `astropy/timeseries` (BLS failures are pre-existing).
