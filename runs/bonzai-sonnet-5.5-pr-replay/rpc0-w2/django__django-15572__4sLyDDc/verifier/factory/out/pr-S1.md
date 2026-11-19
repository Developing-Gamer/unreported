Fix autoreload not restarting when TEMPLATES DIRS contains an empty string

## Overview
Since Django 3.2.4 template dirs are normalized with `cwd / to_path(dir)`. An empty entry (e.g. `"DIRS": os.getenv("TEMPLATES_DIRS", "").split(",")` giving `['']`) became the project root. `template_changed()` then matched the root as a parent of any changed non-`.py` file, reset the loaders and returned True, which tells the reloader the change was handled, so the server did not restart.

## Details
- `django/template/autoreload.py`: `get_template_directories()` now skips empty entries from `engine.dirs` and from `loader.get_dirs()`.
- `tests/template_tests/test_autoreloader.py`: added `test_empty_template_dir_ignored` (DIRS=[''] must not yield the cwd, and `template_changed` on an unrelated file returns None without resetting loaders).

## Verification
- Before the fix: `PYTHONPATH=/testbed python tests/runtests.py template_tests.test_autoreloader` failed with `AssertionError: PosixPath('/testbed') unexpectedly found in {PosixPath('/testbed')}`.
- After the fix: same command, 11 tests OK.
