viewcode: don't write _modules pages for epub when viewcode_enable_epub is False

## Overview
`make html epub` produced `_modules/*.xhtml` pages in the epub output even with `viewcode_enable_epub=False` (the default). The epub build reuses the pickled environment from the html build, which already contains the module data collected by viewcode, and `collect_pages` wrote pages from it without checking the builder.

## Details
- `sphinx/ext/viewcode.py`: new `is_supported_builder()` (false for `singlehtml`, and for `epub*` unless `viewcode_enable_epub`). `doctree_read` already had this check inline; it now uses the helper, and `collect_pages` uses it too.
- Tests: html build followed by an epub build in the same srcdir/doctreedir; asserts no `_modules` directory by default, and that pages are still created with `viewcode_enable_epub=True`.
- CHANGES entry added (the issue number #8609 should be checked against the real issue).

## Verification
- Before: `pytest tests/test_ext_viewcode.py` -> `test_viewcode_epub_disabled_after_html` fails (`_modules` exists in epub output).
- After: 4 pass; `test_viewcode` still fails as it did on the base commit (HTML snippet mismatch, unrelated).
