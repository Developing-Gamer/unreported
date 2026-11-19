Honor allow_redirects=True in requests.head()

## Problem
Some URL checks report 301 instead of the destination's 200 even though redirect following is enabled; direct URLs are fine.

## Cause
`requests.head()` in `requests/api.py` did `kwargs['allow_redirects'] = False`, unconditionally overwriting a caller's explicit `allow_redirects=True`. `get` and `options` (and `Session.head`) use `setdefault`, so only the top-level `head()` was affected.

## Fix
Use `kwargs.setdefault('allow_redirects', False)`: HEAD still does not follow redirects by default, but an explicit `allow_redirects=True` is honoured.

## Verification
- New test `test_head_allow_redirects_override` (local HTTP server, `/old` -> 301 -> `/new` 200; no network needed): `python -m pytest test_requests.py -k head_allow_redirects`. Before the fix it fails (status 301, empty history); after, it passes: `allow_redirects=True` gives 200 with history `[301]`, and the default still gives 301 with empty history.
- Full `test_requests.py`: 93 passed, 1 failed (`test_conflicting_post_params`, TypeError, unrelated to this change).
