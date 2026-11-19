Fix dateformat 'o' (ISO 8601 year) returning the calendar year at year boundaries

**Problem:** The weekly export labelled 2021-01-01 as `2021-53` while the December days of the same ISO week were `2020-53`. `DateFormat.o()` is documented as the ISO year matching `W`, but returned `self.data.year`.

**Fix:** `DateFormat.o()` now returns `self.data.isocalendar()[0]`, consistent with `W` using `isocalendar()[1]`.

**Tests:** Added `test_iso_year` in `tests/utils_tests/test_dateformat.py` (2021-01-01 -> `2020-53`, 2020-12-31 -> `2020-53`, 2018-12-31 -> `2019-1`, mid-year -> `2021-24`). Before the fix it fails (`'2018-1' != '2019-1'`, `'2021-53' != '2020-53'`); after it passes.

Verification: `cd tests && PYTHONPATH=/testbed python runtests.py utils_tests.test_dateformat template_tests.filter_tests.test_date` — 31 tests OK.
