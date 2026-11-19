import pytest

from matplotlib._api.deprecation import (
    MatplotlibDeprecationWarning,
    rename_parameter,
)


def test_legacy_parameter_overrides_forwarded_default():
    @rename_parameter("3.5", "old_scale", "scale")
    def transform(values, scale=1):
        return [value * scale for value in values]

    assert transform([2, 4], scale=3) == [6, 12]

    with pytest.warns(MatplotlibDeprecationWarning, match="has been renamed"):
        legacy_result = transform([2, 4], old_scale=3)
    assert legacy_result == [6, 12]

    with pytest.warns(MatplotlibDeprecationWarning, match="has been renamed"):
        forwarded_result = transform([2, 4], old_scale=3, scale=1)
    assert forwarded_result == [6, 12]
