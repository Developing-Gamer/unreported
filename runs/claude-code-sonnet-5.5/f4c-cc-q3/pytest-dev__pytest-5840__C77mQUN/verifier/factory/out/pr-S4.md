Respect empty string returned by pytest_make_parametrize_id

Root cause: `_idval` in src/_pytest/python.py used `if hook_id:`, so an explicit `""` from the hook was treated like None and fell back to default id generation.

Change: use `if hook_id is not None:`. Added `test_pytest_make_parametrize_id_empty_string` in testing/python/metafunc.py and changelog/5973.bugfix.rst.

Verification: manually confirmed collection ids change from `[a]`/`[b]` (before) to `[0]`/`[1]` (empty ids are de-duplicated) with an empty-returning hook. testing/python/metafunc.py could not be run here because `hypothesis` isn't installed.
