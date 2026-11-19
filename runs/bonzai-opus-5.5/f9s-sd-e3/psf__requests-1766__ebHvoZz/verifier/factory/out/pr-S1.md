Fix HTTPResponse.tell() reporting decoded bytes instead of wire bytes

## Problem
Export download progress (tell() / Content-Length) read over 600% on gzip-encoded CSV exports, though the content was correct.

## Cause
In the vendored urllib3 `HTTPResponse.read()`, `_fp_bytes_read` was incremented after the decoder ran, so `tell()` (documented as bytes pulled over the wire) returned decompressed byte counts.

## Fix
Increment `_fp_bytes_read` right after the raw `self._fp.read(...)`, before decompression. Non-encoded responses are unaffected (decoded == raw).

## Verification
- New test `TestHTTPResponseTell::test_tell_counts_wire_bytes_for_gzip_body` (20,000-row gzip CSV streamed with stream(1024)): fails before the fix, passes after.
- `pytest test_requests.py`: 89 pass; 2 failures (`test_conflicting_post_params`, `test_mixed_case_scheme_acceptable`) are pre-existing and fail identically on the base commit.
