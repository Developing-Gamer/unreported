import numpy as np

from xarray import Variable
from xarray.backends import pseudonetcdf_ as backend
from xarray.backends.common import AbstractDataStore


class MemoryStore(AbstractDataStore):
    def get_variables(self):
        return {
            "forecast_period": Variable(
                ("step",),
                np.array([0, 6, 12], dtype=np.int64),
                {"units": "hours"},
            )
        }

    def get_attrs(self):
        return {}

    def get_dimensions(self):
        return {"step": 3}

    def get_encoding(self):
        return {}

    def close(self):
        pass


def test_duration_decoding_can_be_disabled_independently(monkeypatch):
    store = MemoryStore()

    def open_store(cls, filename, **kwargs):
        return store

    monkeypatch.setattr(
        backend.PseudoNetCDFDataStore, "open", classmethod(open_store)
    )

    with backend.PseudoNetCDFBackendEntrypoint().open_dataset(
        "unused.pnc", decode_times=True, decode_timedelta=False
    ) as ds:
        assert ds["forecast_period"].dtype == np.dtype("int64")
        np.testing.assert_array_equal(ds["forecast_period"].values, [0, 6, 12])
        assert ds["forecast_period"].attrs["units"] == "hours"
