import numpy as np
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1.axes_rgb import RGBAxes


def test_invalid_interpolation_is_not_silently_ignored():
    fig = Figure(figsize=(3, 3))
    panels = RGBAxes(fig, [0.1, 0.1, 0.8, 0.8])
    channel = np.linspace(0, 1, 16).reshape(4, 4)

    error = None
    try:
        panels.imshow_rgb(channel, channel, channel, interpolation="cubic")
    except ValueError as exc:
        error = exc

    assert error is not None, "Invalid interpolation must raise rather than render with defaults"
    assert "interpolation" in str(error)
