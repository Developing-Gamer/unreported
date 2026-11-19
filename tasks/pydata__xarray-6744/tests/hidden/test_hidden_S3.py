import numpy as np
import pytest
import xarray as xr
from xarray.testing import assert_allclose


@pytest.mark.parametrize("kind", ["variable", "dataarray", "dataset"])
def test_allclose_checks_dimension_order(kind):
    values = np.array([[1.0, 2.0], [3.0, 4.0]])
    left = xr.Variable(("row", "column"), values)
    right = xr.Variable(("column", "row"), values.copy())

    if kind == "dataarray":
        left = xr.DataArray(left)
        right = xr.DataArray(right)
    elif kind == "dataset":
        left = xr.Dataset({"reading": left})
        right = xr.Dataset({"reading": right})

    rejected = False
    try:
        assert_allclose(left, right)
    except AssertionError:
        rejected = True

    assert rejected, "Different dimension orders must not compare equal positionally"
