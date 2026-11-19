viewcode: don't create module pages for epub when viewcode_enable_epub is False

## Overview
`make html epub` produced `_modules/` pages in the epub output even though `viewcode_enable_epub` is False (the default). The epub build reuses the pickled environment from the html build, so no documents are re-read and `doctree_read` (which has the epub guard) never runs; `collect_pages` then wrote pages for the module data collected by the html build.

## Details
- `sphinx/ext/viewcode.py`: `collect_pages` now returns early for `singlehtml` and for `epub*` builders when `viewcode_enable_epub` is False, mirroring the guard in `doctree_read`.
- `tests/test_ext_viewcode.py`: builds html then epub on the same source/doctree dir; asserts no `_modules` in the epub output by default, and that pages are still written with `viewcode_enable_epub=True`.
- `CHANGES` entry added.

## Proof
Before: `pytest tests/test_ext_viewcode.py -k epub_after_html` fails (`_modules` exists in epub output). After: passes.

## Verification
`python -m pytest tests/test_ext_viewcode.py`: 4 pass; `test_viewcode` fails identically on the base commit (HTML snippet assertion, unrelated to this change).
