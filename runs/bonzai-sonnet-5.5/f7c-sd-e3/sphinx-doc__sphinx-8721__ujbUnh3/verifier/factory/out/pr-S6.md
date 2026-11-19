Fix viewcode creating module pages for epub when viewcode_enable_epub=False

## Overview
With `make html epub`, the epub output contained `_modules/` pages even though `viewcode_enable_epub` is False (the default). The two builders share one saved environment: the html run fills `env._viewcode_modules`, the epub run skips `doctree_read` (which has the epub guard), but `collect_pages` had no guard and wrote the pages from the saved data.

## Details
- `sphinx/ext/viewcode.py`: `collect_pages` now returns early for `singlehtml` and for epub builders when `viewcode_enable_epub` is False, mirroring `doctree_read`.
- `tests/test_ext_viewcode.py`: new `test_viewcode_epub_after_html` builds html then epub with the same srcdir/doctree dir and asserts no `_modules` dir in the epub output. It failed before the fix (`_modules` existed in the epub outdir) and passes now.
- `CHANGES` entry added.

## Verification
`python -m pytest tests/test_ext_viewcode.py` -> new test passes. `test_viewcode` fails on the base commit too (a warning-regex assertion unrelated to this change).
