Fix server_error hiding errors from a broken 500.html behind the generic "Server Error (500)" page

## Overview
Customers sometimes saw only the plain "Server Error (500)" page instead of the branded one. `server_error()` wrapped both `loader.get_template()` and `template.render()` in one `except TemplateDoesNotExist`. When `500.html` exists but a template it extends or includes is missing, the error is raised during `render()`, was caught, and the generic fallback was returned, which hid the real problem.

## Details
- `django/views/defaults.py`: only `loader.get_template()` is inside the `try`. `template.render()` now runs after it, like `bad_request()` already does. The generic page remains the fallback only when `500.html` itself is missing; a missing custom template name is still re-raised.
- `tests/view_tests/tests/test_defaults.py`: new `test_server_error_broken_template` uses a `500.html` that extends a nonexistent template and asserts `TemplateDoesNotExist` is raised rather than the generic page.

Evidence: customer-support message ev_s2. Not covered by open PR #1000 (dateformat only).

## Verification
- Before the fix: `cd tests && PYTHONPATH=/testbed python runtests.py view_tests.tests.test_defaults` fails with `AssertionError: TemplateDoesNotExist not raised`.
- After the fix: the same command passes; `runtests.py view_tests handlers` gives 199 tests OK (2 skipped).
- No visual change in the product UI; no screenshot proof.
