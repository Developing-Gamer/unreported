Convert the HTTP method to the native string type in PreparedRequest.prepare_method

## Overview
`requests.request(method=u'POST', files=...)` raised `UnicodeDecodeError` on Python 2 when the uploaded file held non-ASCII bytes, while `method='POST'` worked. `prepare_method` only upper-cased the method, so a unicode method reached httplib unchanged. httplib then built a unicode request line and joined it with the byte-string multipart body, which forced an implicit ASCII decode of the body. The method is now converted to the native `str` type, as header names already are.

## Details
- `requests/models.py`: `prepare_method` now does `to_native_string(self.method.upper())`. On Python 3 a bytes method (such as `b'post'`) is now also decoded to `str`.
- `test_requests.py`:
  - `test_prepared_method_is_native_string` is an offline test. It prepares a request with a non-native method (unicode on py2, bytes on py3) and checks that `prep.method == 'POST'` and that its type is native `str`.
  - `test_unicode_method_name_with_binary_file` is the issue's scenario, sent against httpbin.

## Verification
- Python 2.7.18: `test_prepared_method_is_native_string` failed on the base commit with `AssertionError: assert <type 'unicode'> is <type 'str'>` and passes with the fix.
- The full `test_requests.py` gives 88 passed, 1 failed with the fix. The one failure is an SSL `CERTIFICATE_VERIFY_FAILED` error, which also fails on the base commit (86 passed, 1 failed there).
