Coerce HTTP method to a native string to fix UnicodeDecodeError with unicode methods (S3, S5)

## Root cause
On Python 2, `Session.request` and `PreparedRequest.prepare_method` only called `method.upper()`, so `u'POST'` stayed `unicode`. httplib then built the request head as unicode, and `msg += message_body` implicitly decoded a binary body (e.g. a multipart file upload) as ASCII, raising `UnicodeDecodeError` (GitHub issue S3 and the Sentry event S5, same traceback).

## Change
- `requests/sessions.py`: `Session.request` converts `method` with `builtin_str` before upper-casing.
- `requests/models.py`: `PreparedRequest.prepare_method` does the same, so `Request(...).prepare()` and `Session.prepare_request` are covered too.
- `test_requests.py`: added `test_unicode_method_name_is_native_string`, an offline test that a `u'POST'` method with binary file data prepares to a native `str`.

## Verification
Ran with the Python 2.7 testbed env. The new test fails without the fix and passes with it. The full `test_requests.py` run gives 87 passed and 1 failed. The failure, `test_mixed_case_scheme_acceptable`, is an SSL certificate error that also occurs without my changes.

Not fixed: S4 (Content-Length on GET) is already fixed in this checkout. S1, S2 and S6 are not defects in this repository.
