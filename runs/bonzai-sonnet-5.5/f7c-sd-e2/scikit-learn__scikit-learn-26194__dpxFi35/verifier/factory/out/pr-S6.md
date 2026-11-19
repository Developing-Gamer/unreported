FIX VarianceThreshold: use population variance for dense input, matching sparse input

## Overview
`VarianceThreshold` computed dense variances with `np.nanvar(..., ddof=1)` (sample variance) but sparse variances with `mean_variance_axis` (population variance, ddof=0). With a non-zero threshold, the same data could select a different number of columns (e.g. a 0/1 indicator column) depending on whether it was dense or sparse. Dense input now uses ddof=0, so both agree and match the documented "training-set variance".

## Details
- `sklearn/feature_selection/_variance_threshold.py`: `np.nanvar(X, axis=0)`.
- Regression test `test_variance_threshold_dense_sparse_consistent` (csr and csc): on a 5x3 binary matrix with threshold 0.18, dense gave variances [0.3, 0.3, 0.2] versus sparse [0.24, 0.24, 0.16], so the third column was selected only for dense input. Now identical.
- Changelog entry in `doc/whats_new/v1.3.rst`.

## Verification
- `pytest sklearn/feature_selection/tests/test_variance_threshold.py`: new test fails before the fix, passes after.
- `pytest sklearn/feature_selection/tests/`: 239 passed, 7 skipped.
