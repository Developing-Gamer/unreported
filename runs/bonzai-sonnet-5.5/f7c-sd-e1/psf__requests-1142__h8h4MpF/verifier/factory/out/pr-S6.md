Preserve existing percent-escapes when preparing URLs (fixes 403 SignatureDoesNotMatch on presigned links)

## Overview
A small subset of copied download links returned `403 SignatureDoesNotMatch`. `PreparedRequest.prepare_url` passed the URL through `requote_uri`, which decoded percent-escapes of unreserved characters (`%7E` → `~`, `%41` → `A`, `%2D`, `%5F`, `%2E`). Presigned URLs are signed over their exact bytes, so any link containing such an escape was rewritten and its signature no longer matched. Links without those escapes were unaffected, which is why only a few failed.

## Details
- `requote_uri` no longer calls `unquote_unreserved`. It splits the URL on valid `%XX` escapes, keeps them byte-for-byte, and quotes only the text between them (spaces, quotes, braces, non-ASCII...). A `%` that does not begin a valid escape is quoted as `%25`.
- `unquote_unreserved` had a wrong hex check (`str.isalnum()`), so `%zz` raised `ValueError` (and Unicode digits could pass). It now uses `string.hexdigits`.
- Tests added in `test_requests.py`: a presigned-style URL with `%7E %41 %2D %5F %2E %2F` stays byte-identical after `prepare()`; a space/brace is still quoted (`%20`, `%7B`); `%zz` and a trailing `%` don't raise.

## Verification
- `/opt/miniconda3/envs/testbed/bin/python -m pytest test_requests.py -k "percent or illegal_char or double_encoded"`: 3 of the 4 selected tests fail before the change (the escapes are decoded; `%zz` raises `ValueError: invalid literal for int() with base 16: 'zz'`), all 4 pass after.
- Full `test_requests.py`: 39 pass. 3 fail for reasons unrelated to this change (`MockRequest.origin_req_host` on Python 3.9 in the digest tests, SSL certificate verification in `test_links`).

Note: behaviour change: bare invalid `%` sequences are now encoded as `%25` instead of being passed through.
