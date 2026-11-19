Refresh bundled CA bundle so HTTPS verification works for modern roots

## Problem
Sentry: `requests.exceptions.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate` (177 events / 113 users in 7 days).

## Cause
`verify=True` uses `requests/cacert.pem` (via `certs.where()` / `DEFAULT_CA_BUNDLE_PATH`). That bundle was an old Mozilla snapshot (148 certs, many expired) and lacked current roots such as ISRG Root X1 (Let's Encrypt) and DigiCert Global Root G2, so servers chaining to them failed verification.

## Fix
Replace `requests/cacert.pem` with a current Mozilla root bundle (certifi 2023.11.17, 146 roots). No code change.

## Tests
Added `TestBundledCACerts.test_bundle_contains_current_roots`: loads the bundle into an SSLContext and asserts ISRG Root X1 and DigiCert Global Root G2 are present. Fails before (no ISRG Root X1), passes after.
Command: `python -m pytest test_requests.py -k bundle_contains` (Python 3.9 env).
