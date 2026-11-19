Make the default pylint data directory XDG Base Directory compliant

Root cause: `pylint.config.PYLINT_HOME` always defaulted to `~/.pylint.d`, cluttering the home directory.

Change: on non-Windows systems the default is now `$XDG_CACHE_HOME/pylint` (falling back to `~/.cache/pylint`); an already existing legacy `~/.pylint.d` is still used so existing caches keep working, and `PYLINTHOME` still takes precedence. Implemented with the stdlib only — no new `appdirs` dependency (see S3: `ModuleNotFoundError: appdirs` shows what happens when that dependency isn't installed). Directory creation uses `os.makedirs` since the parent may not exist. Updated ENV_HELP, doc/faq.rst, ChangeLog and whatsnew.

Verification: updated `test_pylint_home` and added `test_pylint_home_xdg` (default, XDG_CACHE_HOME, legacy dir) in tests/lint/unittest_lint.py; lint, testutils, extensions and functional tests pass.
