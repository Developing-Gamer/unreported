Fix TypeError "unexpected keyword argument 'strict'" when opening connections on Python 3.4+

## Overview
On Python 3.4+ every first request to a host failed with `TypeError: __init__() got an unexpected keyword argument 'strict'` (766 Sentry events, 11 users). The bundled urllib3 always passed `strict=` to `HTTPConnection`/`HTTPSConnection`, a parameter removed from `http.client` in 3.4. The pool now only passes `strict` on Python versions that support it.

## Details
- `requests/packages/urllib3/connectionpool.py`: new `HTTPConnectionPool._connection_kwargs()` returns `{'strict': self.strict}` only when `sys.version_info < (3, 4)`; used by `HTTPConnectionPool._new_conn` and both branches of `HTTPSConnectionPool._new_conn`. `response.py` already reads `strict` via `getattr`, so is unaffected.
- `test_requests.py`: `test_new_connection_without_strict_support` builds HTTP and HTTPS pool connections without any network call.
- `.travis.yml`: add Python 3.4 so this is exercised by CI.

## Verification
- Reproduction on base (Python 3.9): `python -m pytest test_requests.py -k new_connection` fails with `TypeError: __init__() got an unexpected keyword argument 'strict'` at connectionpool.py:196.
- With the fix the test passes. Full `test_requests.py` on 3.9: 24 passed, 3 failed; the failures are unrelated (`MockRequest.origin_req_host` missing in cookie code on py3.9, httpbin 429, SSL cert verification) and need a separate fix/network.
