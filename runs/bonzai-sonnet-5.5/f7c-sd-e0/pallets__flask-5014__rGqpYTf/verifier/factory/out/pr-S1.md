Add `Vary: Cookie` to responses where the session was accessed but is empty or cleared

## Overview
After signing out (`session.clear()`), the logout response and any response that read an empty session carried no `Vary: Cookie` header. A shared cache or CDN could store such a response and serve it to other requests regardless of their session cookie, so users could still see a signed-in page / username after signing out.

Reported in `account-support`: "After signing out, the live account page still shows my username, and refreshing leaves me signed in."

## Details
- `SecureCookieSessionInterface.save_session` returned early for an empty session (after deleting the cookie if it was modified), before reaching the code that adds `Vary: Cookie`. The `if session.accessed: response.vary.add("Cookie")` block now runs before that check, so it applies to empty/cleared sessions too. Cookie deletion behaviour is unchanged.
- Added `test_session_vary_cookie_empty_session`: reading an empty session gives `Vary: Cookie` with no `Set-Cookie`; logging in then clearing the session gives `Vary: Cookie` and an expired `session` cookie.
- Added a CHANGES.rst entry.

## Proof
Before (base commit): `pytest tests/test_basic.py -k session_vary_cookie` -> `test_session_vary_cookie_empty_session` fails with `BadRequestKeyError` on `rv.headers["Vary"]` (header missing).
After: both `session_vary_cookie` tests pass.

## Verification
`python -m pytest tests -q`: 453 passed, 11 failed, 14 skipped. The same 11 failures (CliRunner / Werkzeug deprecation warnings from the installed package versions) occur on the base commit (452 passed, 11 failed).
