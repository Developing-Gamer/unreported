import pytest

from sphinx.search.nl import SearchDutch


@pytest.mark.parametrize('word', ['boeken', 'BOEKEN', 'boeKEN'])
def test_dutch_stemming_is_case_insensitive(word):
    language = SearchDutch({})
    assert language.stem(word) == 'boek'
