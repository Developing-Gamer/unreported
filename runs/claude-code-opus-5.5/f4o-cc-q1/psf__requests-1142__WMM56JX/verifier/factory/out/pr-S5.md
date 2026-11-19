Close the throwaway Session used by requests.get/post/... helpers

Fixes S5 ("requests leaves a hanging connection for each request").

## Root cause
`requests.api.request`, which backs `requests.get/head/post/...`, built a new `Session()` for each
call and returned without closing it. The session's HTTPAdapter PoolManager kept the keep-alive
socket in its pool, and the socket was only released when garbage collection finally reclaimed the
session. Many quick calls therefore piled up ESTABLISHED sockets and could exhaust small thread-pool
servers (the CherryPy case in the report).

## Change
- `requests/api.py`: use `with sessions.Session() as session:` (Session already implements
  `__enter__`/`__exit__` -> `close()`). This clears the adapters' pool managers when the call
  returns, which closes the idle pooled connections.
- `test_requests.py`: `test_api_request_closes_session` checks that the helper closes its session.

## Verification
- The new test fails on the original code and passes with the change.
- End-to-end with a local server, 10 `requests.get` calls with GC disabled: the process went from
  21 open sockets (one listening, plus client and server ends of each connection) to 2.
- The suite results are as reported in pr-S4.md (failures are unrelated to this change).
