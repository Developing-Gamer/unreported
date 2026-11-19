Fix cleared session being reloaded when the request context is re-pushed

## Overview
After signing out (a view calls `session.clear()`), a streamed response (`stream_with_context`) still saw the old session: the live page showed the username and the session cookie was not deleted, so a refresh stayed signed in. Report: "After signing out, the live account page still shows my username, and refreshing leaves me signed in."

## Cause
`RequestContext.push` only opens the session the first time it is pushed, but tested `if not self.session:`. A cleared session is empty and therefore falsy, so a re-push (done by `stream_with_context` / `copy_current_request_context`) reloaded the old signed cookie into it. The response then no longer expired the cookie.

## Fix
`src/flask/ctx.py`: check `if self.session is None:` so an already-opened (even empty) session is kept. Changelog entry added.

## Proof
Regression test `tests/test_reqctx.py::test_session_cleared_before_stream_with_context` logs in, logs out with `session.clear()` and streams a response.
- Before: fails with `assert b'user: alice' == b'user: anon'`.
- After: passes; the body is `user: anon`, `Set-Cookie` expires the session, and the next request is anonymous.

## Verification
`PYTHONPATH=src python -m pytest tests -q`: 461 passed, 3 failed, 14 skipped. The 3 failures (`test_cli.py` `CliRunner(mix_stderr=False)`, from the installed click version) are unrelated to this change.
