Fix TimeSeries required-column check to enforce leading column order

## Overview
`BaseTimeSeries._check_required_columns` tested `set(required_columns).issubset(self.colnames)`, so it only checked that required columns exist, not that they are the *first* columns. Inserting a column before `time` (`add_column(..., index=0)`) or reordering with `keep_columns` passed silently, although the error message says "expected 'time' as the first column". Related to the misleading-exception report (#13009): the check and its message must agree.

## Details
- `astropy/timeseries/core.py`: compare `self.colnames[: len(required_columns)] != required_columns`, so an error is raised whenever the leading columns are not the required ones, in order. The message already lists the required columns and the actual leading columns.
- Existing `test_required_columns` in `astropy/timeseries/tests/test_sampled.py` covers this (it failed with "DID NOT RAISE" on the base commit at the `add_column(index=0)` case) and the `['time', 'a']` message case.

## Verification
- `python -m pytest astropy/timeseries/tests/test_sampled.py::test_required_columns` — failed before (DID NOT RAISE ValueError), passes after.
- `python -m pytest astropy/timeseries`: only pre-existing `test_bls` failures (warnings/deprecations unrelated to this change).
