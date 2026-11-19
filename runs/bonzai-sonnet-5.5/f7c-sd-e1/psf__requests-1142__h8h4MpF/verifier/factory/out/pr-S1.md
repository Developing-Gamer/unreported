Raise on undecodable gzip/deflate bodies and accept zlib-wrapped deflate

## Overview
The catalog call sometimes returned HTTP 200 with an empty body or only the tail of the JSON. `stream_decompress` swallowed `zlib.error`, dropped the chunk that failed and passed the remaining raw chunks through. A body under 10 KB arrives as one chunk, so the client got an empty body with no error. A larger body lost its first chunk and then yielded undecoded bytes.

The usual trigger is `Content-Encoding: deflate`. RFC 2616 says this means zlib-wrapped data, but `stream_decompress` only accepted raw deflate (`-zlib.MAX_WBITS`). Any server sending the correct format hit the swallowed error.

## Details
- `requests/utils.py`: for `deflate`, look at the first two bytes (buffered, so 1-byte chunks work) and use zlib framing if they are a valid zlib header, otherwise raw deflate. Raw-deflate servers keep working.
- `requests/utils.py`: removed the silent passthrough. A `zlib.error` now raises `ContentDecodingError`, so a bad body never looks like a successful empty or partial one.
- `requests/exceptions.py`: new `ContentDecodingError(RequestException)`.
- Raw deflate whose first two bytes happen to look like a zlib header would be misdetected; this is the usual trade-off and is very rare.
- Behaviour change: a response labelled gzip/deflate whose body is not actually compressed now raises instead of being returned with its first chunk dropped.

## Verification
New `StreamDecompressTestCase` in `test_requests.py` (zlib-wrapped deflate as one chunk and many chunks, raw deflate, gzip, corrupt gzip/deflate expecting an error).

`/opt/miniconda3/envs/testbed/bin/python -m pytest test_requests.py -k StreamDecompress`
- Before the fix: 5 failed (zlib-wrapped deflate returns `b''` as a single chunk and garbage as many chunks; corrupt bodies do not raise).
- After the fix: 7 passed.
