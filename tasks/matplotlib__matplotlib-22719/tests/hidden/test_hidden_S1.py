from io import BytesIO

import pytest

from matplotlib._afm import AFM


def test_fractional_character_advances():
    data = b"""StartFontMetrics 4.1
FontName Custom-Roman
StartCharMetrics 2
C 65 ; WX 612.75 ; N A ; B 0 0 600 700 ;
C 86 ; WX 593.5 ; N V ; B 0 0 590 700 ;
EndCharMetrics
StartKernData
StartKernPairs 1
KPX A V -72.5
EndKernPairs
EndKernData
EndFontMetrics
"""
    font = AFM(BytesIO(data))

    assert font.get_width_char('A') == pytest.approx(612.75)
    assert font.get_width_from_char_name('V') == pytest.approx(593.5)
    assert font.string_width_height('AV')[0] == pytest.approx(1133.75)
    assert font.get_str_bbox_and_descent('AV')[2] == pytest.approx(1133.75)
