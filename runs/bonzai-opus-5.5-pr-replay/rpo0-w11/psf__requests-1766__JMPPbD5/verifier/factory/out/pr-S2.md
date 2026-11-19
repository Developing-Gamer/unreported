Replace stale bundled CA list so HTTPS verification works again

## Overview
`verify=True` requests use Requests' own `requests/cacert.pem`, an old Mozilla snapshot (148 certs, many expired) that lacks today's roots (ISRG/Let's Encrypt, etc.). Servers chaining to them fail with `SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate` (Sentry ev_s2: 177 events, 113 users in 7 days). This replaces the bundle with the current Mozilla root list (certifi's cacert.pem, 146 certs).

## Details
- `requests/cacert.pem`: updated to current Mozilla CA bundle.
- `test_requests.py`: new `test_default_ca_bundle_has_modern_roots` loads `certs.where()` into an `ssl.SSLContext` and asserts ISRG Root X1 is present (fails before, passes after).
- Not changed: `certs.where()` still returns the vendored file; no new certifi dependency (certifi isn't installed in the env).

## Verification
- Before: `test_mixed_case_scheme_acceptable` fails with `ssl.SSLCertVerificationError: ... unable to get local issuer certificate (_ssl.c:1147)`; new bundle test fails (ISRG Root X1 missing).
- After: both pass; `requests.get` on https://letsencrypt.org, https://github.com, https://www.google.com all return 200.
- Full `test_requests.py`: 90 passed, 1 failed (`test_conflicting_post_params`, unrelated TypeError, fails the same on base).
