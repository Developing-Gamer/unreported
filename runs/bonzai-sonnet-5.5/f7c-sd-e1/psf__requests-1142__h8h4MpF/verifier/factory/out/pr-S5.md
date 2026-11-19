Close the session in the simple API so requests.get/head/post don't leave connections open

## Overview
`requests.get`, `head`, `post` and the other top-level helpers each built a new `Session` and never closed it. With the default `stream=False`, the connection went back into that session's pool and stayed open until the session was garbage collected. This ties up server resources. The response object keeps a reference to the adapter and its pool, so the connection can stay open for as long as the response lives.

## Details
- `requests/api.py`: `request()` now uses `with sessions.Session() as session:`, which calls `Session.close()` on return and closes the pooled connections.
- `stream=True` still works: its connection is checked out of the pool. When it is released later, the closed pool closes it instead of re-pooling it.
- `test_requests.py`: new `SimpleApiConnectionTestCase` serves one keep-alive response from a local socket server. It keeps the response alive and asserts the server sees the client close the connection.

## Verification
`/opt/miniconda3/envs/testbed/bin/python -m pytest test_requests.py -k simple_api_closes -q`
- Before: fails with `AssertionError: Lists differ: [False] != [True]` (the connection was still open).
- After: passes.

Full `test_requests.py`: 36 passed, 3 failed (`test_DIGESTAUTH_WRONG_HTTP_401_GET`, `test_DIGEST_HTTP_200_OK_GET`, `test_links`). The same 3 fail with only this change reverted, so they are unrelated to it.
