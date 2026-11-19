Store persistent data in the XDG cache directory instead of ~/.pylint.d

## Root cause
`pylint/config/__init__.py` hard-coded `PYLINT_HOME` to `~/.pylint.d` whenever `PYLINTHOME` was unset. This puts a dot-directory in the user's home instead of the location the XDG Base Directory Specification (or the platform's convention) gives for cached data.

## Change
- When the home directory is known, `PYLINT_HOME` now defaults to `platformdirs.user_cache_dir("pylint")`, which is `$XDG_CACHE_HOME/pylint` or `~/.cache/pylint` on Linux and the platform-native cache directory on macOS and Windows. `PYLINTHOME` still takes precedence. `.pylint.d` in the current directory is still the fallback when no home directory can be found.
- `save_results` now uses `os.makedirs`, so missing parent directories (for example `~/.cache`) are created.
- Added `platformdirs>=2.2.0` to `install_requires`, and updated `ENV_HELP`, `doc/faq.rst` and the ChangeLog.
- This uses `platformdirs` rather than `appdirs`. The production `ModuleNotFoundError: No module named 'appdirs'` (S3) shows `appdirs` cannot be assumed to be installed. S3 itself is not caused by this checkout (nothing here imports appdirs).
- Existing `~/.pylint.d` directories are left in place, not migrated. The only effect is that the "previous run" score comparison starts fresh once.

## Verification
- Updated `tests/lint/unittest_lint.py::test_pylint_home` to expect the platformdirs cache dir.
- Added `test_pylint_home_follows_xdg_cache_home` (Linux only). It checks that `XDG_CACHE_HOME` is honoured and that `save_results`/`load_results` round-trip when the cache directory's parents are missing.
- `pytest tests/lint/unittest_lint.py` passes.
