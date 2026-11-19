import io
import zlib

import pytest

from requests.packages.urllib3.response import HTTPResponse


@pytest.mark.parametrize('encoding,wbits', [
    ('gzip', 16 + zlib.MAX_WBITS),
    ('deflate', zlib.MAX_WBITS),
])
def test_tell_counts_wire_bytes_for_decoded_responses(encoding, wbits):
    payload = b'order_id,status\n' + b'12345,complete\n' * 1000
    compressor = zlib.compressobj(wbits=wbits)
    encoded = compressor.compress(payload) + compressor.flush()
    response = HTTPResponse(
        body=io.BytesIO(encoded),
        headers={'content-encoding': encoding},
        preload_content=False,
    )
    try:
        assert response.tell() == 0
        assert response.read() == payload
        assert response.tell() == len(encoded)
    finally:
        response.close()
