Fix the "o" date format to return the ISO-8601 week-numbering year

## Root cause
`DateFormat.o()` in `django/utils/dateformat.py` is documented as the "ISO 8601 year number matching the ISO week number (W)", but it returned `self.data.year`. For days at a year boundary that belong to a week of the neighboring ISO year, `o` and `W` did not match. For example, 2021-01-01 is in ISO week 53 of 2020, but `"o-W"` rendered it as `2021-53`, while 2020-12-31 in the same week rendered as `2020-53`. This is the mislabeling seen in the weekly export.

## Change
`o` now returns `self.data.isocalendar()[0]`.

## Verification
- Added `DateFormatTests.test_iso_year_format` in `tests/utils_tests/test_dateformat.py`. It covers 2020-12-31, 2021-01-01, 2021-01-03, 2021-01-04, 2018-12-31 (which belongs to ISO year 2019) and a mid-year date. Without the fix it fails for 4 dates; with the fix it passes.
- Ran `runtests.py utils_tests.test_dateformat queryset_pickle template_tests.test_custom model_enums queries`: OK.
