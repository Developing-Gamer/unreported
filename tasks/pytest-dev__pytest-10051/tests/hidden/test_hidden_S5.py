import pytest

from _pytest.faulthandler import get_timeout_config_value


@pytest.mark.parametrize("configured_timeout", ["0.25", "1.75", "2"])
def test_timeout_preserves_fractional_seconds(
    pytestconfig, monkeypatch, configured_timeout
):
    monkeypatch.setitem(
        pytestconfig._inicache, "faulthandler_timeout", configured_timeout
    )

    assert get_timeout_config_value(pytestconfig) == float(configured_timeout)
