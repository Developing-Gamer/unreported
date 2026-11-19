Fix template autoreload breaking when TEMPLATES DIRS contains an empty string

## Root cause
`django.template.autoreload.get_template_directories()` normalizes every configured template dir with `Path.cwd() / to_path(dir)` (this was added for #32744). An empty string, e.g. from `os.getenv("TEMPLATES_DIRS", "").split(",")`, becomes `Path.cwd()`, which is the project root. Then `template_changed()` sees the project root in the parents of every changed non-`.py` file. It resets the loaders and returns `True`, and that stops the autoreloader from restarting the server.

## Change
- `django/template/autoreload.py`: skip empty values from `backend.engine.dirs` and from each loader's `get_dirs()` before normalizing them.

## Verification
- Added `test_template_changed_in_template_directory_empty_dir` and `test_get_template_directories_ignores_empty_dirs` to `tests/template_tests/test_autoreloader.py`. Both fail without the fix and pass with it.
- `./runtests.py template_tests.test_autoreloader utils_tests.test_autoreload`: 93 tests, OK (20 skipped).
