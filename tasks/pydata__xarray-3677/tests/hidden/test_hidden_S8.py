import pytest
import xarray as xr


@pytest.mark.parametrize(
    "object_type,register",
    [
        (xr.DataArray, xr.register_dataarray_accessor),
        (xr.Dataset, xr.register_dataset_accessor),
    ],
)
def test_accessor_initialization_failure_is_reported(object_type, register):
    name = "calibration_probe_for_test"

    class CalibrationAccessor:
        def __init__(self, obj):
            self.units = obj.calibration_units

    register(name)(CalibrationAccessor)
    try:
        valid = object_type(attrs={"calibration_units": "K"})
        assert getattr(valid, name).units == "K"

        missing_metadata = object_type()
        observed_error = None
        try:
            getattr(missing_metadata, name)
        except Exception as exc:
            observed_error = exc

        assert isinstance(observed_error, RuntimeError), (
            "Accessor initialization failure was not reported as a RuntimeError: "
            + repr(observed_error)
        )
        assert "error initializing" in str(observed_error)
    finally:
        delattr(object_type, name)
