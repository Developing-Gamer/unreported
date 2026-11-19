Fix TimeSeries required-column check to verify the columns are first, in order

## Overview
`BaseTimeSeries._check_required_columns` only tested that the required columns were *present* (`set(required).issubset(colnames)`), while its error message says they must be "the first column(s)". So e.g. `ts.add_column(Column(...), index=0)` was silently accepted, leaving `time` no longer first, and the message wording did not match the condition tested.

## Details
- `astropy/timeseries/core.py`: the condition is now `self.colnames[:len(required_columns)] != list(required_columns)`, matching the message. The no-columns branch and relax handling are unchanged.
- `test_sampled.py::test_required_columns` covers adding a column at index 0 (the existing assertion, which failed with "DID NOT RAISE" before the fix) and at index 1 with two required columns, with message text.
- Changelog entry added in `docs/changes/timeseries/`.

## Verification
- `pytest astropy/timeseries/tests/test_sampled.py -k required_columns`: fails on base (DID NOT RAISE), passes after.
- `pytest astropy/timeseries`: the only failures are in `periodograms/bls` (warnings from the environment), unrelated to this change.
