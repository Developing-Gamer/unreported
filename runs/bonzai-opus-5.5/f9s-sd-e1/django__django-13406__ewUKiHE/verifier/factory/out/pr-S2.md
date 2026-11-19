Fix server_error() swallowing TemplateDoesNotExist raised while rendering 500.html

## Overview
Internal-error responses sometimes showed only the generic "Server Error (500)" page instead of the branded 500.html. `server_error()` rendered the template inside the `try/except TemplateDoesNotExist` meant only to detect a missing 500.html, so a TemplateDoesNotExist raised during rendering (e.g. `{% include %}` of a missing partial) was mistaken for a missing 500.html and the generic fallback was returned, hiding the real error.

## Details
- `django/views/defaults.py`: only `loader.get_template()` stays in the `try`; `template.render()` now runs after the except block, as in `bad_request()` and `permission_denied()`.
- `tests/view_tests/tests/test_defaults.py`: regression test with a 500.html that includes a missing template; asserts TemplateDoesNotExist is raised (failed before the fix: "TemplateDoesNotExist not raised").

## Verification
`cd tests && PYTHONPATH=/testbed python runtests.py view_tests.tests.test_defaults handlers`
