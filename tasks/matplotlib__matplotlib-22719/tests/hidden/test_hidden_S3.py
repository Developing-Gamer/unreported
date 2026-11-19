import numpy as np
import pytest

from matplotlib.bezier import (
    inside_circle,
    split_bezier_intersecting_with_closedpath,
)


@pytest.mark.parametrize('tolerance', [1e-2, 1e-3, 1e-4])
def test_split_endpoint_respects_boundary_tolerance(tolerance):
    radius = 1.3
    control_points = np.array([[0.0, 0.0], [4.0, 0.0]])
    left, right = split_bezier_intersecting_with_closedpath(
        control_points, inside_circle(0.0, 0.0, radius),
        tolerance=tolerance,
    )

    np.testing.assert_allclose(left[-1], right[0], rtol=0, atol=1e-14)
    boundary_error = abs(np.linalg.norm(left[-1]) - radius)
    assert boundary_error <= tolerance, (
        f'Split endpoint misses the circle by {boundary_error}, '
        f'exceeding tolerance {tolerance}'
    )
