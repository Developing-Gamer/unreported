Honour allow_redirects in requests.head()

## Overview
URL checks calling `requests.head(url, allow_redirects=True)` reported the 301 instead of the destination's 200, because the module-level `head()` overwrote the caller's `allow_redirects` with `False`. It now only defaults it to `False`, like `Session.head()`. Direct URLs were unaffected; redirecting URLs now follow when asked.

## Before / After
Before: `requests.head(url, allow_redirects=True)` against a local server (HEAD /c -> 301 to /d -> 200) returned 301 (`assert 301 == 200`).
After: returns 200 with one history entry; `requests.head(url)` still returns 301.

## Details
- `requests/api.py`: `kwargs['allow_redirects'] = False` -> `kwargs.setdefault('allow_redirects', False)`.
- `test_requests.py`: `test_head_allow_redirects_is_honoured` uses a local HTTP server (no network needed).

## Verification
`python -m pytest test_requests.py -k test_head_allow_redirects_is_honoured` fails before, passes after.
