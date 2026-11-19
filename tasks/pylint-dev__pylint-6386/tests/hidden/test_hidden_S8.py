import pytest

from pylint.config.options_provider_mixin import OptionsProviderMixIn


class ReportOptions(OptionsProviderMixIn):
    name = "report-options"
    options = (
        ("report-label", {"type": "string", "default": "nightly", "help": "Report label."}),
        ("report-format", {"type": "string", "default": "text", "help": "Report format."}),
    )


@pytest.mark.parametrize("selection", [[], ()])
def test_explicit_empty_option_selection_yields_nothing(selection):
    with pytest.warns(DeprecationWarning, match="OptionsProviderMixIn has been deprecated"):
        provider = ReportOptions()

    assert [name for name, _, _ in provider.options_and_values()] == [
        "report-label", "report-format"
    ]
    assert list(provider.options_and_values(provider.options[:1])) == [
        ("report-label", provider.options[0][1], "nightly")
    ]
    assert list(provider.options_and_values(selection)) == []
