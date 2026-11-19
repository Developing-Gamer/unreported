import xarray as xr
from xarray.util import generate_ops


def test_generated_round_preserves_decimal_keyword(monkeypatch):
    source = "\n".join(generate_ops.render(generate_ops.ops_info, is_module=True))
    namespace = {
        "__name__": "xarray.core._generated_ops_test",
        "__package__": "xarray.core",
    }
    exec(compile(source, "<generated operators>", "exec"), namespace)

    # Exercise the generated wrapper with the library's real array implementation.
    monkeypatch.setattr(
        xr.DataArray, "round", namespace["DataArrayOpsMixin"].round
    )
    data = xr.DataArray([1.234, 5.678], dims="sample")
    expected = xr.DataArray([1.23, 5.68], dims="sample")

    xr.testing.assert_identical(data.round(2), expected)
    xr.testing.assert_identical(data.round(decimals=2), expected)
