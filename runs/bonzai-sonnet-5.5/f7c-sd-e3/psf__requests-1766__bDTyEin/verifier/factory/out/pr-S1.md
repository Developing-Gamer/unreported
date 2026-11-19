Fix HTTPResponse.tell() counting decompressed bytes instead of wire bytes

## Overview
Streaming a gzip/deflate response and computing progress as `tell()/Content-Length` overshot 100% (over 600% for repetitive CSVs), because the bundled urllib3 `HTTPResponse.read()` added the length of the *decoded* data to `_fp_bytes_read`. `tell()` is documented as bytes pulled over the wire, so it now counts the raw bytes read from the connection. Downloaded content is unchanged.

## Before / After
Before (base, `pytest test_requests.py -k ResponseTell`): 2 failed (gzip and deflate: `tell()` equals decompressed size). After: 3 passed.

## Details
- `requests/packages/urllib3/response.py`: increment `_fp_bytes_read` with the raw `len(data)` before decoding; removed the post-decode increment (which also included decoder flush output).
- `test_requests.py`: `ResponseTellTestCase` covers plain, gzip (streamed) and deflate (read all).

## Verification
`python -m pytest test_requests.py` (py3.9 testbed env): 91 passed, 2 failed (`test_conflicting_post_params`, `test_mixed_case_scheme_acceptable`), which fail identically on the base commit.
