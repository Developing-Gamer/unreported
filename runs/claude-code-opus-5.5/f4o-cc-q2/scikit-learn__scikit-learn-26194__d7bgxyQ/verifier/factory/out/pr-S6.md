Make VarianceThreshold compute the same variance for dense and sparse input

## Root cause
`VarianceThreshold.fit` computed the variance of sparse input with `mean_variance_axis` (population variance, `ddof=0`) but of dense input with `np.nanvar(X, axis=0, ddof=1)` (unbiased variance). On a dense input every variance was therefore inflated by n/(n-1). On small batches this factor is large enough that a feature just below the threshold, such as a binary indicator column, gets selected when the data is dense but not when the same data is sparse. This matches the production report (S6): one extra selected indicator column for dense vs sparse input.

## Change
- `sklearn/feature_selection/_variance_threshold.py`: use `np.nanvar(X, axis=0)` (`ddof=0`), consistent with the sparse path and with the documented `variances_`.
- Changelog entry in `doc/whats_new/v1.3.rst`.

## Verification
- New test `test_variance_threshold_dense_sparse_consistency` covers CSR, CSC and BSR. It checks that `variances_` and `get_support()` match between dense and sparse input on a 4-sample binary dataset where the old code selected an extra column. It fails on the old code and passes with the fix.
- `pytest sklearn/feature_selection` passes.
