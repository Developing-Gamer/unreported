Fixed autoreload ignoring changes when TEMPLATES DIRS contains an empty string

## Overview
Since Django 3.2.4, `get_template_directories()` normalizes each `DIRS` entry as `cwd / to_path(dir)`. An empty string (e.g. `os.getenv("TEMPLATES_DIRS", "").split(",")` giving `['']`) therefore became the project's working directory. `template_changed()` then treated every non-`.py` file change in the project as a template change and returned `True`, which suppressed the autoreloader restart, and `watch_for_template_changes()` watched the whole project tree.

## Details
- `django/template/autoreload.py`: skip falsy entries in `backend.engine.dirs` and in loader `get_dirs()` results.
- `tests/template_tests/test_autoreloader.py`: two regression tests with `DIRS=['']`. One asserts cwd is not in `get_template_directories()`. The other asserts `template_changed()` returns `None` and does not call `reset_loaders` for a non-template file in the project.

Reproduction: the new tests fail on the base commit (`AssertionError: PosixPath('/testbed') unexpectedly found in {PosixPath('/testbed')}` and `True is not None`) and pass with the fix.

## Verification
`PYTHONPATH=/testbed python tests/runtests.py template_tests.test_autoreloader utils_tests.test_autoreload --parallel=1`: 93 tests OK (23 skipped).
