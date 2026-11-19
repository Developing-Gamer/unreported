Fix TypeError "unexpected keyword argument 'strict'" when opening connections on Python 3.4+

## Overview
Every first connection to a host raised `TypeError: __init__() got an unexpected keyword argument 'strict'` (766 events, 11 users in 7 days). The bundled urllib3 passed `strict=` to `HTTPConnection`/`HTTPSConnection`, a parameter `http.client` removed in Python 3.4. Connections are now created without `strict` on 3.4+ and still receive it on older Pythons.

## Details
- `requests/packages/urllib3/connectionpool.py`: new `HTTPConnectionPool._conn_kwargs()` returns `{}` on Python >= 3.4 and `{'strict': self.strict}` otherwise; used by `HTTPConnectionPool._new_conn` and both branches of `HTTPSConnectionPool._new_conn`. `response.py` already reads `strict` via `getattr`, so it is unaffected.
- `test_requests.py`: `NewConnectionTestCase` builds HTTP and HTTPS connections from a pool without any network call.
- `.travis.yml`: add Python 3.4 so this is exercised in CI.

## Verification
- Before: `python -m unittest test_requests.NewConnectionTestCase` (Python 3.9) fails with `TypeError: __init__() got an unexpected keyword argument 'strict'` in `_new_conn`.
- After: the same command passes (2 tests).
- Not run on Python 2.x (no interpreter available); that path is unchanged.
