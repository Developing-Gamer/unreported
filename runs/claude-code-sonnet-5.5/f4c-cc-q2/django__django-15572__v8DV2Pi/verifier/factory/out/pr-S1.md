Ignore empty strings in TEMPLATES DIRS when watching templates for autoreload

Root cause: `django.template.autoreload.get_template_directories()` normalizes each template dir with `cwd / to_path(dir)`. An empty string (e.g. from `"".split(",")`) therefore becomes the current working directory, so `template_changed()` saw every changed non-.py file under the project as a template change and returned True, which prevented the autoreloader from restarting on code changes.

Change: skip falsy entries in `engine.dirs` and in loader `get_dirs()` results when collecting template directories.

Verification: added `test_empty_template_dir_ignored` in `tests/template_tests/test_autoreloader.py`; ran `python tests/runtests.py template_tests.test_autoreloader`.
