import pytest

from requests.packages.charade.chardistribution import EUCTWDistributionAnalysis


def test_euctw_confidence_for_mixed_frequency_characters():
    analyzer = EUCTWDistributionAnalysis()
    analyzer.reset()
    # Eight frequent characters and twelve characters outside the frequent set.
    characters = (
        [b'\xc4\xa1'] * 4
        + [b'\xc4\xf3'] * 4
        + [b'\xc4\xa2'] * 12
    )
    for character in characters:
        analyzer.feed(character, 2)

    assert analyzer.get_confidence() == pytest.approx(8.0 / (12 * 0.75))
