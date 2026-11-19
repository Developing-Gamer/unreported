Quote the qop value in the Digest Authorization header

## Overview
`HTTPDigestAuth` sent `qop=auth` as a bare token while every other string directive in the header (username, realm, nonce, uri, response, opaque, algorithm, cnonce) was quoted. Some servers expect the quoted form, as the GitHub issue reports. The header now sends `qop="auth"`.

## Before / After
Before (base, `pytest test_requests.py -k QOP_IS_QUOTED`): 1 failed, because the header contained `qop=auth`. After: 1 passed.

## Details
- `requests/auth.py`: `build_digest_header` emits `qop="auth"`. `nc` stays unquoted, as RFC 2617 defines it as an unquoted token.
- `test_requests.py`: `test_DIGEST_AUTH_QOP_IS_QUOTED` builds a header from a fixed challenge and checks for `qop="auth"` and an unquoted `nc`.
- Note: RFC 2617 gives the request-side `message-qop` as a token. The quoted `qop-options` the issue cites is the server's challenge. Quoting the value is still accepted by compliant servers, and this follows the upstream project's change.

## Verification
`python -m pytest test_requests.py -k "DIGEST or digest"` (py3.9 testbed env): 6 passed, including the existing digest tests against httpbin.
