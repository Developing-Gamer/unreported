Convert the HTTP method to the native string type in PreparedRequest.prepare_method

## Evidence
GitHub issue: on Python 2.7.2, `requests.request(method=u'POST', ..., files=files)` raises UnicodeDecodeError, while `method='POST'` works.

## Cause
`prepare_method` only called `.upper()`, so a unicode method stayed `unicode` on Python 2. Building the multipart body with a unicode method forces an implicit ASCII decode of the binary file content. (On Python 3 the analogous case is a `bytes` method, which stayed `bytes`.)

## Fix
`self.method = to_native_string(self.method.upper())` in `PreparedRequest.prepare_method`. All paths (Session.request, Request.prepare, Session.prepare_request) go through it. `to_native_string` was already imported.

## Proof / verification
- New test `test_unicode_method_name` fails on the base commit (`assert b'POST' == 'POST'`) and passes with the fix.
- `python -m pytest test_requests.py -q -k unicode_method_name`
- Full `test_requests.py`: 86 passed, 2 failed (`test_conflicting_post_params`, `test_mixed_case_scheme_acceptable`); the same 2 fail on the base commit (Python 3.11 incompatibilities). Python 2 was not available, so the original UnicodeDecodeError was reproduced only through its Python 3 analogue (a bytes method).
