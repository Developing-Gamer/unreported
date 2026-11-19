Convert the HTTP method to the native string type in PreparedRequest.prepare_method

## Overview
On Python 2, `requests.request(method=u'POST', ..., files={...})` raised `UnicodeDecodeError` when the uploaded file contained non-ASCII bytes, while `method='POST'` worked. `prepare_method` only upper-cased the method, so a unicode method reached httplib unchanged; httplib then built a unicode request header block and concatenated the binary multipart body to it, forcing an ASCII decode. The method is now converted to the native `str` type.

## Details
- `requests/models.py`: `prepare_method` now does `to_native_string(self.method.upper())` (header names were already converted this way). On Python 3 a `bytes` method is likewise decoded to `str`.
- `test_requests.py`: `test_prepared_method_is_native_string` checks that `u'post'` and `b'post'` prepare to a native-`str` `'POST'`. It needs no network.

## Proof
Run with the Python 2.7.18 env (`/opt/miniconda3/envs/testbed/bin/python -m pytest test_requests.py -q -k prepared_method`):
- Before: fails at `assert type(pr.method) is type('')` (method stays `unicode`).
- After: passes.

## Verification
Full `test_requests.py` on Python 2.7: 89 passed, 1 failed. The failure is an SSL certificate-verification error that needs the network. It is unrelated to this change and also fails on the base commit. No httpbin network access was available to run the original upload end to end.
