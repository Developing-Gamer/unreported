viewcode: do not generate module pages for epub when viewcode_enable_epub is False

Root cause: the `viewcode_enable_epub` and singlehtml checks were only in `doctree_read`. With `make html epub` the html build leaves `_viewcode_modules` in the pickled environment. `collect_pages` then ran for epub and wrote module pages regardless of the setting.

Change: `collect_pages` now returns early for singlehtml, and for epub builders when `viewcode_enable_epub` is False. Added a CHANGES entry.

Verification: added `test_viewcode_epub_default` and `test_viewcode_epub_enabled` in tests/test_ext_viewcode.py. They build html then epub in the same environment. The default test fails before the fix and passes after. `test_viewcode` already fails in this checkout without my change.
