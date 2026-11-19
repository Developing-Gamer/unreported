import numpy as np
import pandas as pd
import seaborn.objects as so

from seaborn._marks.base import resolve_color


def test_explicit_rgba_opacity_is_preserved_for_multiple_points():
    rgba = (0.2, 0.4, 0.6, 0.25)
    mark = so.Dot(color=rgba, alpha=0.85)
    data = pd.DataFrame({"x": [0, 1, 2], "y": [1, 3, 2]})

    np.testing.assert_allclose(resolve_color(mark, {}), rgba)
    np.testing.assert_allclose(
        resolve_color(mark, data),
        np.tile(rgba, (len(data), 1)),
    )
