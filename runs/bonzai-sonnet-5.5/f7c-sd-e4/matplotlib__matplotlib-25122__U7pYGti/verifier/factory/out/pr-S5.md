Fix window normalisation in mlab._spectral_helper for windows with negative values

## Overview
`mlab._spectral_helper` normalised by `np.abs(window).sum()` (magnitude/complex modes and psd with `scale_by_freq=False`). For windows with negative lobes such as flattop, `sum(abs(w)) != sum(w)`, so amplitudes/powers were scaled wrongly (a constant signal gave 0.858 instead of 1 at DC). scipy uses the signed `window.sum()`.

## Details
- Use `window.sum()` instead of `np.abs(window).sum()` in the magnitude, complex and non-`scale_by_freq` psd branches.
- Use `(window**2).sum()` (equivalent to the old abs form, for real windows).
- Added `test_spectral_helper_window_negative_values` using a flattop window.

## Verification
- New test fails before the fix (0.857984 != 1) and passes after.
- `pytest lib/matplotlib/tests/test_mlab.py` (2425 passed); spectrum/psd/csd/specgram tests in test_axes.py (9 passed).
