Quote the qop value in Digest Auth Authorization header (RFC 2617)

## Root cause
`HTTPDigestAuth.build_digest_header` (requests/auth.py) built the `Authorization` header with `qop=auth` as a bare token. Strict server implementations expect a quoted string, as curl sends (`qop="auth"`), and they reject the unquoted form. (RFC 2617's grammar for the response's `message-qop` is actually a bare token; the quoting is for compatibility with servers and clients that read the spec that way.)

## Change
- `requests/auth.py`: send `qop="auth"` instead of `qop=auth`. The digest calculation is unchanged: the response hash still uses the unquoted `auth` value.
- `test_requests.py`: add `test_DIGEST_AUTH_QUOTES_QOP_VALUE`, an offline test. It sets a challenge on `HTTPDigestAuth` and checks that the generated header contains `qop="auth"`, for both the `qop="auth"` and `qop="auth,auth-int"` challenges.

## Verification
- The new test fails on the original code and passes with the fix.
- Full `test_requests.py` run: 89 passed, 2 failed. The 2 failures (`test_conflicting_post_params`, `test_mixed_case_scheme_acceptable`) happen the same way without this change and have nothing to do with it.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
