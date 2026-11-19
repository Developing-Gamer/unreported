Fix window normalization in mlab._spectral_helper for windows with negative values

## Overview
`mlab._spectral_helper` normalised spectra by `np.abs(window).sum()`. For windows with negative samples (e.g. flattop) this is larger than the true coherent gain, so `magnitude_spectrum`, `complex_spectrum`, and `psd`/`csd` with `scale_by_freq=False` returned values too small (a unit sine on a 512-point flattop gave a magnitude peak of 0.4287 instead of 0.5). Normalization now uses `window.sum()` (and `(window**2).sum()` for the density case), matching SciPy.

## Details
- `lib/matplotlib/mlab.py`: drop the `np.abs` in the magnitude, complex and non-`scale_by_freq` PSD normalizations; `(window**2).sum()` replaces `(np.abs(window)**2).sum()` (identical for real windows).
- `lib/matplotlib/tests/test_mlab.py`: new `test_spectral_window_with_negative_values` using a flattop window; it fails before the fix (magnitude peak 0.4287 vs 0.5) and passes after.
- Non-negative windows (hann, etc.) are unaffected.

## Verification
`/opt/miniconda3/envs/testbed/bin/python -m pytest lib/matplotlib/tests/test_mlab.py -q -k negative_values` fails before and passes after; test_mlab.py and the spectral tests in test_axes.py pass (2434 passed).
