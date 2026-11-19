viewcode: do not create module pages for epub when viewcode_enable_epub=False

## Root cause
`sphinx/ext/viewcode.py` skipped epub builders (unless `viewcode_enable_epub` is set) only in `doctree_read`, which collects `env._viewcode_modules`. `collect_pages` had no such check. With `make html epub`, the epub build reuses the pickled environment that the html build already filled. `doctree_read` does not run again for unchanged docs, so `collect_pages` found the html-collected modules and wrote `_modules/*.xhtml` pages into the epub.

## Change
Added the same guards to `collect_pages` that `doctree_read` uses: return early for `singlehtml`, and for `epub*` builders when `viewcode_enable_epub` is False.

## Verification
New tests in `tests/test_ext_viewcode.py`:
- `test_viewcode_epub_default`: epub build with the default config produces no `_modules/spam/mod1.xhtml`. It fails before the fix because the environment is shared with the html test build, which is the same situation as `make html epub`.
- `test_viewcode_epub_enabled`: with `viewcode_enable_epub=True`, the module page is still produced.
- `test_viewcode_epub_after_html`: after an html build fills `env._viewcode_modules`, `collect_pages` on an epub builder yields nothing.

The new tests fail before the change and pass after. `test_viewcode` fails both before and after the change, and the failure is unrelated: a source-highlighting markup assertion in this environment.
