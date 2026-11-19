Fix deprecated `_request_ctx_stack` alias returning the app context stack

## Overview
Accessing the deprecated `flask.globals._request_ctx_stack` returned the *app* context stack. Because every CLI command runs in an app context, monitoring/extension code checking `_request_ctx_stack.top` saw a non-None value and reported `requests_in_progress=1` for the whole scheduled job on CLI-only workers, though no request existed.

## Details
- `src/flask/globals.py`: module `__getattr__` now returns `__request_ctx_stack` for `_request_ctx_stack`.
- `tests/test_reqctx.py`: regression test — inside only `app.app_context()`, `top` is `None`; inside `test_request_context()`, it is the `RequestContext`.
- `CHANGES.rst`: bugfix entry.

## Verification
- New test fails on the base commit (`top` is an `AppContext`) and passes after the fix.
- `PYTHONPATH=src python -m pytest tests/test_reqctx.py -k deprecated_request`; full `tests` suite run.
