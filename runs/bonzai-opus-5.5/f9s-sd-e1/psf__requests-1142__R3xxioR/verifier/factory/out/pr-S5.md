Close the session created by the simple API so requests.get/post/... leave no open socket

## Overview
`requests.get()`, `head()`, `post()` and friends build a throwaway `Session` for every call and never closed it. With the default `stream=False` the keep-alive socket went back into that session's private pool and stayed open until the garbage collector removed the session, which ties up server resources (GitHub issue, also #458). The simple API now closes its session before returning.

## Details
- `requests/api.py`: `request()` uses `with sessions.Session() as session:`; `Session.close()` clears the adapters' PoolManager, which closes pooled sockets. Connections still checked out (`stream=True`) are not in the pool; urllib3 closes them when released into the closed pool, after the body is read, so streaming still works.
- `test_requests.py`: `test_simple_api_closes_connections` (gc disabled, 5 `requests.get` calls against a local threaded HTTP/1.1 keep-alive server, asserts no client sockets remain open; fails before the fix with `AssertionError: 1 != 0`) and `test_simple_api_stream_still_readable` (iter_content and content with `stream=True` still return the full body).

## Verification
`/opt/miniconda3/envs/testbed/bin/python -m pytest test_requests.py -k simple_api`: fails before the fix, passes after. Full file: 32 pass, 3 fail (test_links, two digest tests) which need external network/httpbin and are unrelated.
