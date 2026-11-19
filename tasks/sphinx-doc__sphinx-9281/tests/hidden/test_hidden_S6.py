import pytest

from sphinx.util.texescape import escape_abbr


@pytest.mark.parametrize('separator', [' ', '\t', '\n', '\r\n'])
def test_abbreviation_spacing_across_source_whitespace(separator):
    text = 'See fig.' + separator + '2 for details'
    expected = r'See fig.\@{}' + separator + '2 for details'
    assert escape_abbr(text) == expected
