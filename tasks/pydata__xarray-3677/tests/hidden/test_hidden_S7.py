import dask.array as da
import numpy as np

from xarray.core.dask_array_ops import rolling_window


def test_centered_even_window_alignment():
    values = np.arange(12, dtype=float)
    chunked = da.from_array(values, chunks=(4,))

    actual = rolling_window(
        chunked, axis=0, window=4, center=True, fill_value=np.nan
    ).compute()

    padded = np.pad(values, (2, 1), mode="constant", constant_values=np.nan)
    expected = np.stack([padded[i:i + 4] for i in range(len(values))])

    np.testing.assert_array_equal(actual, expected)
