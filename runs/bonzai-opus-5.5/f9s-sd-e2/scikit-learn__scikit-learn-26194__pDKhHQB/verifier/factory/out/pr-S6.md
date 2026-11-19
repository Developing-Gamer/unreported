Fix VarianceThreshold giving different supports for dense and sparse input

## Overview
`VarianceThreshold.fit` used `np.nanvar(X, axis=0, ddof=1)` (divide by n-1) for dense input but `mean_variance_axis` (divide by n) for sparse input. On small batches, dense variances were inflated by n/(n-1), so an indicator column with variance just below the threshold was kept for dense input and dropped for sparse input. Dense now uses the population variance, matching sparse and the documented behaviour.

## Evidence
Support channel report: the same small batch yields one extra selected column as a dense table versus a sparse matrix.
With X=[[1,0,1],[1,0,0],[1,1,0],[0,0,1]], threshold=0.2: before, dense variances were [0.25, 0.25, 0.333] and support [True, True, True]; sparse gave [False, False, True].

## Details
- `sklearn/feature_selection/_variance_threshold.py`: drop `ddof=1`.
- New test `test_variance_threshold_dense_sparse_consistent` (CSR and CSC) fails before the fix (support mismatch) and passes after.
- Changelog entry in `doc/whats_new/v1.3.rst` (PR number is a placeholder to be set on opening).

## Verification
`pytest sklearn/feature_selection/tests/test_variance_threshold.py` and the common estimator checks for VarianceThreshold: 50 passed.
