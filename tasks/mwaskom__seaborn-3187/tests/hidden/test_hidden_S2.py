import numpy as np
import pandas as pd
import pytest

from seaborn._core.groupby import GroupBy
from seaborn._core.moves import Dodge


@pytest.mark.parametrize("orient", ["x", "y"])
def test_dodge_gap_preserves_mark_centers(orient):
    other = {"x": "y", "y": "x"}[orient]
    data = pd.DataFrame({
        orient: [0.0, 0.0, 1.0, 1.0],
        other: [2.0, 4.0, 3.0, 5.0],
        "color": ["a", "b", "a", "b"],
        "width": [0.8, 0.8, 0.8, 0.8],
    })

    result = Dodge(gap=0.5)(
        data, GroupBy([orient, "color"]), orient, {}
    )

    np.testing.assert_allclose(result["width"], [0.2, 0.2, 0.2, 0.2])
    np.testing.assert_allclose(result[orient], [-0.2, 0.2, 0.8, 1.2])
