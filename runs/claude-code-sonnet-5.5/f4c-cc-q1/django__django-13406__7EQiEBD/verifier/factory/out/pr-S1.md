Fix 'o' date format to return the ISO 8601 year

Root cause: `DateFormat.o()` returned `self.data.year` (calendar year) rather than the ISO year matching the ISO week number from `W`. For dates such as 2021-01-01 (ISO week 53 of 2020) this produced '2021-53' instead of '2020-53'.

Change: `o()` in django/utils/dateformat.py now returns `self.data.isocalendar()[0]`. Added `test_iso_year_format` in tests/utils_tests/test_dateformat.py covering year-boundary dates in both directions.

Verification: ran utils_tests.test_dateformat; the new test fails without the fix and passes with it.
