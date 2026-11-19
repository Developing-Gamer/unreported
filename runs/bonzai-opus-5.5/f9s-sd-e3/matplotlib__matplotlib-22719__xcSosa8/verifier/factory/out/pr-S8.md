No pull request: empty data on a category axis is already fixed by #1002

The deprecation warning comes from `StrCategoryConverter.convert`. `all()` of an empty array is True, so empty input takes the deprecated "numbers pass through" branch. Open PR #1002 already changes that check to `if values.size and is_numlike:` and adds regression tests in `lib/matplotlib/tests/test_category.py`. The working tree already contains the same change. I made no further change.
