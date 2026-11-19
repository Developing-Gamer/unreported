Fix dateformat 'o' specifier to return the ISO 8601 week-numbering year

## Overview
The weekly export labelled 2021-01-01 as `2021-53` while the December days of the same week were `2020-53`. `DateFormat.o()` is documented as the ISO-8601 year matching `W`, but returned the calendar year. Around New Year, `o-W` therefore mixed calendar year with ISO week.

## Details
- `django/utils/dateformat.py`: `o()` now returns `self.data.isocalendar()[0]`, the same source `W()` uses for the week number.
- `tests/utils_tests/test_dateformat.py`: added `test_iso_year_matches_iso_week` with year-boundary cases (2020-12-31, 2021-01-01, 2019-12-30, 2008-12-29, 2010-01-03, and a mid-year date).

## Verification
`PYTHONPATH=/testbed python tests/runtests.py utils_tests.test_dateformat`: the new test fails on the base commit (4 subtests, e.g. `'2021-53' != '2020-53'`) and passes after the fix. `template_tests.filter_tests.test_date` also passes.
