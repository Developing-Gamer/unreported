Fix BaseEngine.template_dirs so DIRS take precedence over app template dirs

## Overview
Receipt emails rendered through the Jinja2 or TemplateStrings backends fell back to the bundled app template even though a custom template with the same name existed in `DIRS`. `BaseEngine.template_dirs` put the installed apps' template directories *before* the configured `DIRS`, so the bundled template was found first. `DIRS` are now searched first, matching the DjangoTemplates backend (filesystem loader, then app_directories).

## Details
- `django/template/backends/base.py`: `template_dirs = template_dirs + get_app_template_dirs(...)` instead of the reverse.
- New test `test_dirs_take_precedence_over_app_dirs` (in `tests/template_backends/test_dummy.py`, inherited by the Jinja2 and DjangoTemplates test classes) with a fixture `tests/template_backends/dirs/template_backends/hello.html` that shadows the app's `hello.html`. It asserts `template_dirs[0]` is the DIRS entry and that the DIRS template is rendered.

## Verification
- Before the fix: the new test fails for the dummy, Jinja2 and Django classes (`PosixPath('.../jinja2') != '.../dirs'`).
- After: `cd tests && python runtests.py template_backends` passes.
- `template_tests` has one failure, `test_loaders.FileSystemLoaderTests.test_permissions_error`; it fails the same way on the base commit (the tests run as root, so the permission error is not raised).
