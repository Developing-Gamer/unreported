Quote the qop value in Digest Auth Authorization header

Root cause: `HTTPDigestAuth.build_digest_header` emitted `qop=auth` unquoted. RFC 2617 requires the qop value in the client's response to be sent as a quoted string (as curl does), and some servers reject the unquoted form.

Change: `requests/auth.py` now emits `qop="auth"`. Added `test_DIGEST_qop_value_is_quoted` in `test_requests.py`, which builds the header offline from a canned challenge and asserts the quoted form.

Verification: the new test passes under the testbed Python (`pytest test_requests.py -k qop_value`). Tests that need httpbin were not run, since there is no network.
