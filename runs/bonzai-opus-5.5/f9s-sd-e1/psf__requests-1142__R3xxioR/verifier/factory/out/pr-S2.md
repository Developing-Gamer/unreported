Stop passing `strict` to stdlib HTTP(S) connections on Python 3

## Overview
Every request made on Python 3.4+ failed with `TypeError: __init__() got an unexpected keyword argument 'strict'` before reaching the network (766 events, 11 users in 7 days; stack: `sessions.request` -> `adapters.send` -> `connectionpool.urlopen` -> `_get_conn`). The bundled urllib3 always passed `strict=` to `http.client.HTTPConnection`/`HTTPSConnection`, and Python 3.4 removed that parameter. Requests now open connections normally on Python 3.

## Details
- `requests/packages/urllib3/connectionpool.py`: new `HTTPConnectionPool._connection_kwargs()` builds `host`/`port` and adds `strict` only when `not six.PY3`. `HTTPConnectionPool._new_conn` and both constructions in `HTTPSConnectionPool._new_conn` (`HTTPSConnection` and `VerifiedHTTPSConnection`) use it. Python 2 behaviour is unchanged.
- `requests/packages/urllib3/_collections.py`: import `MutableMapping` from `collections.abc` (falling back to `collections` on Python 2). Without it the package does not import at all on Python 3.10+, which is a separate failure of the same kind.
- `test_requests.py`: `test_connection_pool_opens_connection` builds a connection from both an HTTP and an HTTPS pool.

Open PR #1000 (mislabelled gzip bodies, `requests/utils.py`) touches different code and does not cover this.

## Verification
`/opt/miniconda3/envs/testbed/bin/python -m pytest test_requests.py -k test_connection_pool_opens_connection` (Python 3.9)
- before: fails with `TypeError: __init__() got an unexpected keyword argument 'strict'` at `connectionpool.py:196`
- after: passes

Also `requests.head`/`requests.get` against a local `http.server` return 200. Full `test_requests.py`: 28 passed, 3 failed (before the fix: 21 failed, 5 passed). The 3 remaining failures are unrelated and are outside this change: two digest-auth tests (`MockRequest` has no `origin_req_host` on newer Python) and `test_links` (needs network and a certificate that verifies).
