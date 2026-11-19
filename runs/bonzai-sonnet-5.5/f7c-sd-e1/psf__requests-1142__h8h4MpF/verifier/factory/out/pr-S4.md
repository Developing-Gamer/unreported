Don't send Content-Length: 0 on body-less GET and HEAD requests

## Overview
Every prepared request got `Content-Length: 0` when it had no body, including GET and HEAD. Some servers (amazon.com in the report) answer such GETs with a 503. GET and HEAD requests without a body now carry no `Content-Length` header. Other methods (e.g. POST) without a body still send `Content-Length: 0`.

## Details
- `PreparedRequest.prepare_content_length` in `requests/models.py` set `Content-Length` to `'0'` before looking at the body. The default is now set only in a final branch, when the body is `None` and the method is not GET/HEAD. `prepare_method` runs before `prepare_body`, so the method is known. The seek/tell and `len(body)` branches and the streaming path are unchanged; `prepare_auth` calls the same function, so it follows the same rule.
- Tests added in `test_requests.py`: no `Content-Length` for body-less GET and HEAD; `'0'` for POST without data; `'5'` for POST with `data='hello'`.

## Verification
- Before the fix `test_no_content_length_for_get_and_head` fails (`AssertionError: False is not true`); after it, it passes along with the two POST tests.
- `python -m pytest test_requests.py` in the testbed env: 35 passed, 3 failed. The failures are unrelated to this change: two digest-auth tests (`'MockRequest' object has no attribute 'origin_req_host'`) and `test_links` (SSL certificate verification failure).
