Fix window normalization in mlab._spectral_helper for windows with negative values

`_spectral_helper` normalized with `np.abs(window).sum()` for the magnitude, complex and `psd(scale_by_freq=False)` modes. For windows with negative lobes (e.g. flattop) `sum(|w|) != sum(w)`, so amplitudes/power were scaled wrongly (a constant signal's DC magnitude came out as 0.857 instead of 1 with a flattop window). The signed `window.sum()` is now used, as in scipy. `(np.abs(window)**2).sum()` was simplified to the equivalent `(window**2).sum()`.

Test: `test_window_with_negative_values` in `lib/matplotlib/tests/test_mlab.py` (flattop window, magnitude_spectrum, complex_spectrum, psd with scale_by_freq=False). It failed before the fix (0.857408 != 1) and passes after.

Verification: `python -m pytest lib/matplotlib/tests/test_mlab.py lib/matplotlib/tests/test_axes.py -k "mlab or spectrum or psd or csd or specgram or negative or cohere"` -> 2437 passed.
