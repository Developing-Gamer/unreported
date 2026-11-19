from xarray.backends import plugins
from xarray.backends.common import BackendEntrypoint


class NetCDF4Backend(BackendEntrypoint):
    available = True
    open_dataset_parameters = ("filename_or_obj",)

    def guess_can_open(self, filename_or_obj):
        return isinstance(filename_or_obj, str) and filename_or_obj.endswith(".nc")


class H5NetCDFBackend(NetCDF4Backend):
    pass


def test_automatic_selection_preserves_standard_backend_priority(monkeypatch):
    # Both installed readers recognize this input, so their priority matters.
    monkeypatch.setattr(
        plugins,
        "BACKEND_ENTRYPOINTS",
        {"h5netcdf": H5NetCDFBackend, "netcdf4": NetCDF4Backend},
    )
    engines = plugins.build_engines([])
    monkeypatch.setattr(plugins, "list_engines", lambda: engines)

    assert plugins.guess_engine("climate.nc") == "netcdf4"
