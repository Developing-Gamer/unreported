Fixed autoreload ignoring changes when TEMPLATES DIRS contains an empty string

Since Django 3.2.4, `django.template.autoreload.get_template_directories()` normalizes each DIRS entry with `cwd / to_path(dir)`. An empty string (e.g. from `os.getenv("TEMPLATES_DIRS", "").split(",")`) therefore became the current working directory, so `template_changed()` treated every non-.py file change in the project as a template change, returned True and suppressed the autoreloader's restart. `watch_for_template_changes()` also watched the whole project tree.

Fix: skip empty entries in `engine.dirs` and in loader `get_dirs()` results.

Tests: added `test_empty_string_in_dirs_is_ignored` and `test_non_template_changed_with_empty_string_in_dirs` to `tests/template_tests/test_autoreloader.py`; they fail before the fix and pass after.

Verification: `cd tests && PYTHONPATH=/testbed python runtests.py template_tests.test_autoreloader utils_tests.test_autoreload` (93 tests OK).
