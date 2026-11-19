Keep the body of mislabelled gzip/deflate responses instead of dropping its first chunk

## Overview
Some catalog responses are sent with `Content-Encoding: gzip` (or `deflate`) but the body is not compressed. `Response.content` then came back empty (bodies under 10 KB) or without its first 10 KB (larger bodies), with HTTP 200 and no error. Retrying worked only when the server happened to label the response correctly. The full body is now returned.

## Details
`stream_decompress` in `requests/utils.py` fell back to passing raw data through on `zlib.error`, but it only yielded what was left in the iterator. The chunk that had just failed to decompress, and any chunk read before it, were lost. `Response.content` reads in 10 KB chunks, so the first 10 KB was gone.

The fix keeps the raw chunks read until the decompressor has produced output. On `zlib.error` with no output yet, it yields those chunks and then the rest of the iterator. Real compressed bodies are unaffected. An error after output has already been produced still behaves as before.

Tests added to `test_requests.py` (offline, no httpbin):
- mislabelled gzip and deflate bodies, under and over 10 KB, round-trip unchanged
- a real gzip body still decodes
- `list(stream_decompress(iter([b'abc', b'def']))) == [b'abc', b'def']`

## Verification
`/opt/miniconda3/envs/testbed/bin/python -m pytest test_requests.py -k "mislabelled or real_gzip or passes_through"`
- before the fix: 3 failed, 1 passed (the real-gzip test)
- after the fix: 4 passed

The other tests in `test_requests.py` need network access (httpbin) and fail the same way on the base commit.
