Don't send Content-Length on bodiless GET/HEAD requests

Fixes S4 ("requests.get is ALWAYS sending content length").

## Root cause
`PreparedRequest.prepare_content_length` (requests/models.py) started by unconditionally setting
`Content-Length: 0` and only overwrote it when there was a body. So every request, including plain
`requests.get(url)`, went out with `Content-Length: 0`. Some servers (the report cites amazon.com)
answer 503 to a GET that carries the header.

## Change
- `requests/models.py`: set `Content-Length` from the body when there is one (unchanged). For a
  `None` body, send `Content-Length: 0` only when the method is not GET or HEAD. A bodiless
  POST/PUT/PATCH/DELETE still sends `Content-Length: 0`, and a GET that does carry data still gets
  its real length.
- `test_requests.py`: `test_no_content_length` (GET/HEAD prepared without the header) and
  `test_content_length_for_bodiless_post` (POST still gets `0`; GET with data gets the real length).

## Verification
- The new tests fail on the original code and pass with the change.
- End-to-end against a local `http.server`: before, the server received `Content-Length: 0` on
  every `requests.get`; after, no Content-Length header is received.
- `test_requests.py` on py3.9: 26 passed, 4 failed. The 4 failures are environmental and unrelated:
  the py3.9 cookie `MockRequest.origin_req_host` gap, the outdated bundled CA file, and flaky live
  httpbin.org.
