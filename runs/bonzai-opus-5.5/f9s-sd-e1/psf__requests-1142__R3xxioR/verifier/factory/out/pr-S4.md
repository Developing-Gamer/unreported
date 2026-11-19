Don't send Content-Length on bodiless GET/HEAD requests

## Overview
Every `requests.get(...)` carried `Content-Length: 0`, even with no body. Some servers (amazon.com in the report) answer such GETs with 503. GET and HEAD requests with no body now go out without a `Content-Length` header.

## Details
- `PreparedRequest.prepare_content_length` set `Content-Length` to `'0'` unconditionally and `prepare_body`/`prepare_auth` both called it. It now sets the header from the body (seek/tell or `len`) when there is one, and falls back to `'0'` only when there is no body and the method is not GET/HEAD. Empty POST/PUT keep `Content-Length: 0`.
- Tests added in `test_requests.py`: GET/HEAD (with and without `auth`) have no `Content-Length`; empty POST (with and without auth) has `'0'`; POST with `data='abc'` has `'3'`.

## Verification
`python -m pytest test_requests.py -k content_length`: before the fix `test_no_content_length_on_bodiless_get_and_head` fails (header is `'0'`); after it, 2 passed. Full file: the remaining failures (`test_links`, digest-auth tests) also fail on the base commit (network/environment).
