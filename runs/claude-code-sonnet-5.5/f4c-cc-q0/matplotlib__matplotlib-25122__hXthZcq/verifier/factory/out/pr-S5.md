Fix window correction in mlab._spectral_helper for windows with negative values

Root cause: for `scale_by_freq=False` PSD, the result was divided by `np.abs(window).sum()**2`. The correct normalization (as in scipy) is `window.sum()**2`; the absolute value gives wrong results for windows with negative samples such as flattop.

Change: use `window.sum()**2` in that branch of `_spectral_helper`. Other modes are untouched.

Verification: added `test_psd_windowarray_negative_values_no_scale_by_freq` in test_mlab.py (a constant signal must give DC power 1); fails before, passes after; ran test_mlab.py.
