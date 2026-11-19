Fix window correction in mlab._spectral_helper for windows with negative values

## Root cause
`mlab._spectral_helper` divides by `np.abs(window).sum()` to correct for the window: in `magnitude` and `complex` mode, and in `psd` mode when `scale_by_freq=False` (using the square). The correct factor is the coherent gain, `window.sum()`, as in SciPy's `_spectral_helper`. The two values are equal only when the window is non-negative. For windows with negative values, such as flattop, the `np.abs` makes the denominator too large, so the amplitude and power come out too low.

## Change
- Replace `np.abs(window).sum()` with `window.sum()` in the `magnitude`, `complex`, and `psd` (`scale_by_freq=False`) branches.
- Leave `(np.abs(window)**2).sum()` unchanged. It is the correct noise-power normalization for the density scaling and is also right for complex windows.
- Add `TestSpectral.test_psd_window_flattop`. It builds a flattop window (which has negative values) and checks two things: that the `scale_by_freq=False` and `scale_by_freq=True` PSDs are consistent (`spec * win.sum()**2 == spec_a * Fs * (win**2).sum()`), and that a flattop magnitude spectrum keeps the peak amplitude of an unwindowed one.

## Verification
- `pytest lib/matplotlib/tests/test_mlab.py`: all 2490 tests pass, including the new ones.
- Without the fix, 12 of the new parametrized cases fail.
- `pytest lib/matplotlib/tests/test_axes.py -k "psd or spectrum or specgram or csd"`: 9 passed. These image tests use non-negative windows, so their output does not change.
