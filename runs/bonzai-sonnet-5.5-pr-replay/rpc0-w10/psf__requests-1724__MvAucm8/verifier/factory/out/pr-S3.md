Convert the HTTP method to a native string (fixes UnicodeDecodeError with unicode method on Python 2)

## Evidence
GitHub issue: `requests.request(method=u'POST', ..., files={u'file': open(..., 'rb')})` raises `UnicodeDecodeError` on Python 2.7.2, while `method='POST'` works.

## Cause
`Session.request` and `PreparedRequest.prepare_method` only called `.upper()` on the method, so on Python 2 a `unicode` method stayed `unicode`. httplib then builds the request head as unicode and appends the binary multipart body, implicitly decoding the body as ASCII.

## Fix
Pass the upper-cased method through `to_native_string` in `Session.request` and `PreparedRequest.prepare_method` (covers direct `Request`/`PreparedRequest` users too).

## Verification
- New test `test_unicode_method_name` fails before the fix (method is `unicode` on Py2.7) and passes after.
- Full `test_requests.py` on Python 2.7: only `test_mixed_case_scheme_acceptable` fails (SSL cert verification, same on the base commit).
