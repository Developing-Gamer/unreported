Fix window normalization in mlab._spectral_helper for windows with negative values

## Overview
`mlab._spectral_helper` normalized magnitude, complex and non-`scale_by_freq` PSD output by `np.abs(window).sum()`. For windows with negative samples (e.g. flattop) this exceeds the true coherent gain `window.sum()`, so spectra came out too small (for a 512-point flattop and a unit sine: magnitude peak 0.4287 instead of 0.5, about 14% low). Non-negative windows (Hann, etc.) are unaffected.

## Details
- Replace `np.abs(window).sum()` with `window.sum()` (magnitude, complex, and squared for PSD with `scale_by_freq=False`), matching scipy.signal.
- Write the `scale_by_freq` branch as `(window**2).sum()` (identical for real windows).
- Add `test_spectral_window_with_negative_values` using a flattop window: magnitude, complex and PSD (`scale_by_freq=False`) peaks of a unit-amplitude sine must be 0.5.

## Verification
- New test fails before the fix (magnitude peak 0.428693 vs 0.5) and passes after.
- `pytest lib/matplotlib/tests/test_mlab.py`: 2425 passed.
