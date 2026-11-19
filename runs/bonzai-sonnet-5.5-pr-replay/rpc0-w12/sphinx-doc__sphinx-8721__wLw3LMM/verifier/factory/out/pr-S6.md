viewcode: don't generate module pages for epub when viewcode_enable_epub is False

## Problem
With `make html epub`, the html and epub builders share one saved environment. The html run fills `env._viewcode_modules`. The epub run skips `doctree_read` because `viewcode_enable_epub` is False, but `collect_pages` never checked the option. It found the saved data and wrote `_modules/` pages into the epub.

## Fix
`collect_pages` now returns early for `singlehtml` and for `epub*` builders when `viewcode_enable_epub` is False. These are the same guards `doctree_read` already has.

## Tests
Added to `tests/test_ext_viewcode.py`:
- `test_viewcode_epub_after_html`: builds html, then epub in the same srcdir. It failed before the fix (`_modules/spam/mod1.xhtml` existed) and passes now.
- `test_viewcode_epub_enabled`: with `viewcode_enable_epub=True` the pages are still generated.

`python -m pytest tests/test_ext_viewcode.py`: 4 pass. `test_viewcode` fails with and without this change (an alabaster/pygments output mismatch).
