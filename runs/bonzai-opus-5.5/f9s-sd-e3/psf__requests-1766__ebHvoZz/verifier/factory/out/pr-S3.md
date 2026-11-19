Quote the qop value in the Digest Authorization header

## Problem
GitHub issue: "quote qop options in Digest Auth". Strict servers reject a client Authorization header with an unquoted `qop=auth`.

## Cause
`HTTPDigestAuth.build_digest_header` in `requests/auth.py` wrote `, qop=auth, nc=..., cnonce="..."`, so `qop` was the only directive emitted without double quotes.

## Fix
Emit `qop="auth"`. The digest computation is unchanged. Note: RFC 2617's request-header grammar technically gives `qop` as an unquoted token; this change follows the issue's request, and the existing httpbin round-trip tests still pass with the quoted form.

## Verification
- New test `test_DIGEST_QOP_IS_QUOTED` (`python -m pytest test_requests.py -k DIGEST_QOP_IS_QUOTED`): fails before the fix (`assert 'qop="auth"' in header`), passes after.
- `python -m pytest test_requests.py -k "DIGEST or digest"`: 6 passed, including the httpbin digest round trips.
