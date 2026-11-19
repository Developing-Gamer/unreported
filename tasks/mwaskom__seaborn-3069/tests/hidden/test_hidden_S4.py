import numpy as np

from seaborn import widgets
from seaborn.palettes import color_palette


def test_updated_colormap_uses_current_endpoints_for_out_of_range_values():
    cmap = widgets._init_mutable_colormap()
    colors = np.column_stack([color_palette("Reds", 256), np.ones(256)])

    widgets._update_lut(cmap, colors)

    expected_endpoints = colors[[0, -1]]
    np.testing.assert_allclose(cmap([0.0, 1.0]), expected_endpoints)
    np.testing.assert_allclose(cmap([-0.1, 1.1]), expected_endpoints)
