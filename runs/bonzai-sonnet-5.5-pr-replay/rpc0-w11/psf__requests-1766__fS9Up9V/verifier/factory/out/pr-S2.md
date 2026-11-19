Refresh vendored CA bundle so Let's Encrypt (ISRG Root X1) chains verify

**Evidence:** Sentry `requests.exceptions.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate` — 177 events / 113 users in 7 days.

**Cause:** With `verify=True`, `HTTPAdapter.cert_verify` uses only `requests/cacert.pem` (via `certs.where()`). That vendored bundle was a 2013 snapshot: it lacked ISRG Root X1 (and other modern roots) and still contained the expired DST Root CA X3. Any server whose chain ends at a newer root fails to verify.

**Fix:** Replace `requests/cacert.pem` with the current Mozilla root store (146 roots; includes ISRG Root X1, no DST Root CA X3). No code changes; the bundle is the only thing the default verification path reads.

**Tests (test_requests.py, `CABundleTestCase`):** bundle contains ISRG Root X1; bundle does not contain DST Root CA X3; `requests.get('https://letsencrypt.org')` succeeds (needs network).

**Before:** all 3 new tests fail; `requests.get('https://letsencrypt.org')` raises the SSLError above.
**After:** all 3 pass; full `test_requests.py` 92 passed, 1 failed (`test_conflicting_post_params`, unrelated, fails identically on base).

**Follow-up (not done):** the bundle will go stale again; consider letting `certs.where()` prefer certifi/system store when available.
