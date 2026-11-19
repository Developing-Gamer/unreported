import pytest

from matplotlib._fontconfig_pattern import parse_fontconfig_pattern


@pytest.mark.parametrize("pattern", [
    "DejaVu Sans-12.5.4",
    "DejaVu Sans-",
])
def test_malformed_font_size_is_rejected(pattern):
    error = None
    try:
        parse_fontconfig_pattern(pattern)
    except ValueError as exc:
        error = exc
    assert error is not None, f"Invalid font pattern was accepted: {pattern!r}"
