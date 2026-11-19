Don't pass `strict` to stdlib HTTP(S)Connection on Python 3

## Overview
On Python 3.4+ every requests call (get/head/post/put) failed with `TypeError: __init__() got an unexpected keyword argument 'strict'` (766 Sentry events, 11 users in 7 days). The bundled urllib3 connection pools always passed `strict=` to `http.client.HTTPConnection`/`HTTPSConnection`, and that parameter was removed in Python 3.4. The pools now pass `strict` only on Python 2.

## Evidence
Sentry ev_s2: `TypeError: __init__() got an unexpected keyword argument 'strict'`, raised from `urllib3/connectionpool.py` `_get_conn` -> `_new_conn`, reached from `sessions.py send` / `adapters.py send`.

## Details
- `connectionpool.py`: new `HTTPConnectionPool._conn_kw()` returns `{}` on Python 3 and `{'strict': self.strict}` on Python 2. It is used by `HTTPConnectionPool._new_conn` and by both the `HTTPSConnection` and `VerifiedHTTPSConnection` paths in `HTTPSConnectionPool._new_conn`.
- `_collections.py`: import `MutableMapping` from `collections.abc` (falling back to `collections`) so the module imports on Python 3.10+.
- Not changed: `requests/cookies.py` still uses `collections.MutableMapping`, which breaks on 3.10+. It is outside this report.
- `test_requests.py`: added `test_connection_pool_opens_connections`, which builds connections from an HTTP and an HTTPS pool. It needs no network.

## Verification
- Reproduction command: `/opt/miniconda3/envs/testbed/bin/python -m pytest test_requests.py -k test_connection_pool_opens_connections` (Python 3.9). Before the fix it failed with `TypeError: __init__() got an unexpected keyword argument 'strict'` at connectionpool.py:196. After the fix it passes.
- Full `test_requests.py`: 21 failed before, 3 failed after (24 passed). The three remaining failures are `test_DIGESTAUTH_WRONG_HTTP_401_GET`, `test_DIGEST_HTTP_200_OK_GET` and `test_links`. They failed before the fix too, and I did not investigate them. They appear to depend on live httpbin/GitHub or on Python 3 behaviour in the digest tests.
- Python 2 was not run (not available); the `strict` argument is still passed there.
