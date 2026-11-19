Ignore empty template directories in the template autoreloader

## Overview
Since Django 3.2.4, `get_template_directories()` normalizes each `TEMPLATES["DIRS"]` entry with `cwd / to_path(dir)`. An empty string (e.g. `os.getenv("TEMPLATES_DIRS", "").split(",")` gives `['']`) becomes the current directory, i.e. the project root. `template_changed()` then finds that root among the parents of any changed non-`.py` file, resets the loaders and returns `True`, which tells the reloader the change was handled, so the autoreloader no longer restarts the server.

## Details
- `django/template/autoreload.py`: skip falsy entries from `backend.engine.dirs` and from `loader.get_dirs()`.
- `tests/template_tests/test_autoreloader.py`: add `test_empty_template_dir_ignored` with `DIRS=[""]`; it asserts the cwd is not a template directory and `template_changed()` returns `None` for an unrelated file.

## Verification
- Before the fix the new test fails: `AssertionError: PosixPath('/testbed') unexpectedly found in {PosixPath('/testbed')}`.
- After: `PYTHONPATH=/testbed python tests/runtests.py template_tests.test_autoreloader --parallel 1` passes (11 tests, 3 skipped for missing jinja2).
