import pytest

from requests.utils import stream_decompress


@pytest.mark.parametrize('chunks', [
    [b'{"status":"ok","count":3}'],
    [b'{"status":', b'"ok","count":3}'],
])
def test_uncompressed_body_survives_gzip_fallback(chunks):
    expected = b''.join(chunks)

    actual = b''.join(stream_decompress(iter(chunks), mode='gzip'))

    assert actual == expected
