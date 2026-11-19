Coerce HTTP method to native string to avoid UnicodeDecodeError on Python 2

Fixes S3; also resolves S5 (same UnicodeDecodeError raised from httplib `endheaders` in production).

## Root cause
`PreparedRequest.prepare_method` only upper-cased the method. On Python 2, passing `method=u'POST'`
left `PreparedRequest.method` as `unicode`. httplib builds the request line/headers from the method,
so the header block becomes `unicode`; in `_send_output` it then does `msg += message_body`, and when the
body is a byte string containing non-ASCII bytes (e.g. a multipart file upload) Python 2 tries to
ASCII-decode it and raises `UnicodeDecodeError`.

## Change
`requests/models.py`: `prepare_method` now returns `to_native_string(self.method.upper())`, so the method
is always the native `str` type (bytes on Py2, text on Py3). This covers both `Request.prepare()` and
`Session.prepare_request()` / `Session.request()`, which all go through `prepare_method`.

## Verification
- New test `test_unicode_method_name_is_native_string` (offline) asserts that a `u'post'` method becomes native `'POST'`
  through both `Request.prepare()` and `Session.prepare_request()`. It fails before the change
  (`type(prep.method)` is `unicode` on Py2.7) and passes after.
- Full `test_requests.py` on Python 2.7: 87 passed, 1 failed. The failure, `test_mixed_case_scheme_acceptable`,
  is an SSL certificate-verification error on a live network call and fails the same way without this change.
