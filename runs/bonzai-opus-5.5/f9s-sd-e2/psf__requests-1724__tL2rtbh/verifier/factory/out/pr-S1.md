Build each redirect hop from the previous hop, not the original request

## Overview
`Session.resolve_redirects` copied the caller's original `PreparedRequest` on every hop and reset the method from it. After a 303 turned a POST into a GET and cleared the body, a following 307 restored the original POST and its body, so a completion request was re-sent to the redirect target. The target can answer that with an empty success instead of the unknown-job response, which workers then counted as acknowledged.

## Details
- `requests/sessions.py`: after sending each hop, set `req = prepared_request` so the next hop copies the previous hop's method, body and headers. Method changes (303/302 to GET) and the cleared body/Content-Length now carry through the rest of the chain.
- `test_requests.py`: two offline tests using a fake adapter.
  - POST -> 303 -> 307 -> 200 sends POST, GET, GET with no body (before the fix: POST, GET, POST with the body).
  - POST -> 307 -> 200 still re-sends the POST with its original body to the new location.

## Verification
- Before the fix: `test_redirect_303_then_307_stays_get` fails with `AssertionError: assert ['POST', 'GET', 'POST'] == ['POST', 'GET', 'GET']`.
- After the fix: both new tests pass.
- Full `test_requests.py` (Python 2.7 testbed env): 88 passed, 1 failed. The failure is an SSL certificate verification error that needs the network. It fails the same way on the base commit.
