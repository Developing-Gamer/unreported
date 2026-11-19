Store pylint run data in the XDG cache directory instead of ~/.pylint.d

## Overview
Pylint created a `.pylint.d` folder in every user's home directory, ignoring the XDG Base Directory Specification. Run data now goes to the platform user cache directory (`$XDG_CACHE_HOME/pylint`, default `~/.cache/pylint` on Linux). `PYLINTHOME` still overrides it.

## Details
- `pylint/config/__init__.py`: `PYLINT_HOME` defaults to `platformdirs.user_cache_dir("pylint")` when a home directory exists (the `.pylint.d` fallback in the current directory when no home is found is unchanged). `save_results` uses `os.makedirs(..., exist_ok=True)` because the new path is nested. `ENV_HELP` updated.
- `setup.cfg`: add `platformdirs>=2.2.0` to `install_requires`.
- `doc/faq.rst` (3.2) and `ChangeLog` updated. The old `~/.pylint.d` is no longer read or written; stale stats there are only cache and can be deleted.
- Tests: `test_pylint_home` now expects the platformdirs location; new `test_pylint_home_follows_xdg_cache_home` checks `save_results` writes `$XDG_CACHE_HOME/pylint/mod1.stats` and creates no `~/.pylint.d`.

## Verification
- Before the fix: `pytest tests/lint/unittest_lint.py -k pylint_home` fails (`PYLINT_HOME` is `.../home/.pylint.d`, expected `.../home/.cache/pylint`).
- After: passes; `pytest tests/lint tests/test_self.py tests/test_func.py` gives 173 passed.
