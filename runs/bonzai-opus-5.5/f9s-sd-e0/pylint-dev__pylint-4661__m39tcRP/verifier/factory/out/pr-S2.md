Store pylint's persistent data in the user cache directory (XDG compliant)

## Problem
Pylint created a `~/.pylint.d` directory in the user's home folder to store run data, ignoring the XDG Base Directory Specification (issue: "Make pylint XDG Base Directory Specification compliant").

## Fix
- `pylint/config/__init__.py`: when `PYLINTHOME` is not set and a home directory exists, `PYLINT_HOME` is now `platformdirs.user_cache_dir("pylint")` (`$XDG_CACHE_HOME/pylint`, i.e. `~/.cache/pylint`, on Linux). `PYLINTHOME` still overrides; the `.pylint.d` fallback in the cwd when no home is found is kept.
- `save_results` uses `os.makedirs(..., exist_ok=True)`, since the standard location is a nested path that `os.mkdir` cannot create (the save silently failed).
- `platformdirs` added to `install_requires`; `ENV_HELP`, `doc/faq.rst` (3.2) and the ChangeLog updated.
- Existing `~/.pylint.d` data is no longer used (it is only a cache of previous stats) and can be removed.

## Tests
- `test_pylint_home` now expects `platformdirs.user_cache_dir("pylint")`.
- New `test_save_results_creates_nested_home` checks saving/loading under a nested, not-yet-existing directory.
Both fail on the base commit and pass now; `tests/lint/unittest_lint.py` and `tests/test_self.py` pass (157 passed).
