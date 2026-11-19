import pytest

from astropy.time import Time


@pytest.mark.parametrize("axis", [1, -1])
def test_squeeze_rejects_non_singleton_axis(axis):
    times = Time([[59000.0, 59001.0, 59002.0]], format="mjd", scale="tai")
    assert times.squeeze(axis=0).shape == (3,)

    error = None
    try:
        times.squeeze(axis=axis)
    except ValueError as exc:
        error = exc

    assert error is not None, "Squeezing a non-singleton axis must raise ValueError"
