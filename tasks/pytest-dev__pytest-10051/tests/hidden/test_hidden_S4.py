import pytest

from _pytest.compat import ascii_escaped


@pytest.mark.parametrize("value", [b"device\x7fready", "device\x7fready"])
def test_del_is_escaped_in_parameter_text(value):
    assert ascii_escaped(value) == r"device\x7fready"
