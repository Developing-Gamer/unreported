Fix VarianceThreshold selecting different features for dense and sparse input

## Root cause
For dense input `VarianceThreshold.fit` used `np.nanvar(X, axis=0, ddof=1)` (sample variance), while sparse input uses `mean_variance_axis`, which gives the population variance. A feature with variance between the two values was kept for dense input and dropped for sparse input, so dense input could select one extra column.

## Change
The dense path now uses the population variance (`np.nanvar(X, axis=0)`), matching the sparse path and the documented behavior, in `sklearn/feature_selection/_variance_threshold.py`. A changelog entry is added. `variances_` for dense input is now smaller by a factor of (n-1)/n.

## Verification
- Added `test_variance_threshold_dense_sparse_consistent`, covering CSR and CSC. It uses a column whose population variance is 0.1875 and sample variance is 0.25, with threshold 0.2.
- Ran `pytest sklearn/feature_selection sklearn/metrics`; all pass.
