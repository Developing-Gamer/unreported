Fix TypeError on `strict` kwarg with Python 3.4+; stop sending Content-Length on GET/HEAD; close simple-API sessions

Sources: S2 (primary), S4, S5 (bundled in one PR for convenience; they have separate root causes, listed below).

## Root cause
- S2: `HTTPConnectionPool._new_conn` (and the HTTPS variants) always passed `strict=` to `http.client` connections. That argument was removed in Python 3.4, so every request fails with `TypeError: __init__() got an unexpected keyword argument 'strict'`.
- S4: `PreparedRequest.prepare_content_length` unconditionally set `Content-Length: 0` for body-less requests, so every GET/HEAD carried the header; some servers (amazon.com) answer 503.
- S5: `requests.api.request` built a throwaway `Session` and never closed it, so pooled sockets stayed open until garbage collection.

## Change
- `connectionpool.py`: new `_conn_kwargs()` passes `strict` only when `sys.version_info < (3, 4)`; used by all three `_new_conn` paths.
- `models.py`: `Content-Length: 0` is only added for body-less methods other than GET/HEAD.
- `api.py`: `request()` closes the session in a `finally` (in-flight streamed responses are unaffected; their connections are not in the pool).

## Verification
Added `LocalServerTestCase` in `test_requests.py` (local HTTP server, no network): 4 tests fail before the change and pass after (Python 3.9). The other existing tests need httpbin.org and were not run offline.

Not fixed: S1, S3, S6 (no actionable library defect; see triage.json).
