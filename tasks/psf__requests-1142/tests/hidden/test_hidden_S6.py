import pytest

from requests.packages.urllib3.util import parse_url


@pytest.mark.parametrize('url, expected', [
    ('https://files.example.test/download?', '/download?'),
    ('https://files.example.test/download?#preview', '/download?'),
    ('https://files.example.test?', '/?'),
    ('https://files.example.test/download?token=abc', '/download?token=abc'),
    ('https://files.example.test/download', '/download'),
])
def test_request_uri_preserves_explicit_empty_query(url, expected):
    assert parse_url(url).request_uri == expected
