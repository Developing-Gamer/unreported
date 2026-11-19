Fix TruncatedSVD explained_variance_ratio_ for sparse input

Root cause: for sparse X, `TruncatedSVD.fit_transform` used `mean_variance_axis(X, axis=1)` (per-row variance) to compute total variance, while the dense branch uses per-feature variance (`np.var(X, axis=0)`). The denominator was wrong, so the ratio was off for sparse input; the transformed embedding itself was unaffected.

Change: use `axis=0` in `sklearn/decomposition/truncated_svd.py`. Added `test_explained_variance_ratio_sparse_matches_dense`.

Verification: new test fails before the fix (ratios ~0.43x of the dense ones) and passes after; `pytest sklearn/decomposition/tests/test_truncated_svd.py` passes.
