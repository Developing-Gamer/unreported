Refresh bundled CA certificates (add ISRG Root X1, drop expired DST Root CA X3)

## Overview
HTTPS requests to servers whose chain ends at a newer root (e.g. Let's Encrypt's ISRG Root X1) failed with `SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate` (177 events / 113 users in 7 days). Requests verifies only against its vendored `requests/cacert.pem`, which dated from 2013, lacked modern roots and still contained the expired DST Root CA X3. The bundle is replaced with the current Mozilla root store, so `requests.get('https://letsencrypt.org')` verifies by default.

## Before / After
Before: `requests.get('https://letsencrypt.org')` raises the exact SSLError above; `pytest test_requests.py -k CABundle` fails 2 of 2 (no ISRG Root X1, DST Root CA X3 present).
After: the same request returns 200; `-k CABundle` passes 2 of 2.

## Details
- `requests/cacert.pem`: replaced with the Mozilla root store as shipped by certifi 2023.11.17 (146 roots; the old file had 148 from 2013). Same PEM-with-comments format as before, so nothing in `certs.py`/`adapters.py` changes.
- `test_requests.py`: `CABundleTestCase` asserts the bundle contains ISRG Root X1 and does not contain DST Root CA X3 (offline, no network needed).
- Not done: making `certs.where()` prefer certifi/system store. That adds a dependency/behaviour change; a vendored bundle will go stale again, so it needs periodic refreshes.

## Verification
`python -m pytest test_requests.py` (py3.9 testbed env): 94 passed, 1 failed (`test_conflicting_post_params`, fails identically on the base commit). Live check: `requests.get('https://letsencrypt.org')` -> 200.
