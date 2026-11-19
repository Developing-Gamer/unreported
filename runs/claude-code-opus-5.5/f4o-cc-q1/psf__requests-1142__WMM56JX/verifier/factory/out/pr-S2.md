urllib3: stop passing removed `strict` kwarg to http.client on Python 3

Fixes S2 (Sentry: `TypeError: __init__() got an unexpected keyword argument 'strict'`, 766 events).

## Root cause
The vendored urllib3 (`requests/packages/urllib3/connectionpool.py`) built connections with
`HTTPConnection(host=..., port=..., strict=self.strict)`, and did the same for `HTTPSConnection` and
`VerifiedHTTPSConnection`. Python 3.4 removed `strict` from `http.client`, so on modern interpreters
`_new_conn` raises TypeError and every request fails. The frame list in the Sentry event is jumbled
(the api.py frames are listed after urllib3 and are out of order), but the exception and the
`connectionpool.urlopen` -> `_get_conn` path match the code exactly. The error reproduces with
`HTTPConnectionPool('localhost', 80)._new_conn()`.

## Change
- Added `HTTPConnectionPool._conn_kw()`, which returns `{'strict': self.strict}` on Python 2 and
  `{}` on Python 3. It is used at all three connection construction sites. This is the same approach
  upstream urllib3 took. The pool's public `strict` argument is unchanged.
- `test_requests.py`: `test_new_connection_does_not_pass_unsupported_kwargs` (creates HTTP and HTTPS
  connections without network I/O).

## Verification
- The new test fails with the TypeError before the change and passes after it.
- Before the change, every network test in `test_requests.py` failed with this TypeError on
  py3.9. After it, real requests to a local server succeed and most network tests pass (26 passed,
  4 failed). The remaining failures have separate environmental causes: py3.9 cookie
  `MockRequest.origin_req_host`, an outdated CA bundle, and live httpbin.org flakiness.
