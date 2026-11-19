Fix TruncatedSVD explained_variance_ratio_ for sparse input

## Overview
For sparse input, `TruncatedSVD.fit_transform` computed the total variance with `mean_variance_axis(X, axis=1)` (per-row variances) while the numerator `explained_variance_` and the dense branch use per-feature variances. The ratio was therefore wrong for sparse matrices only (about 8% relative off in the test data), while the embedding coordinates (`U * Sigma`) were unaffected. This matches the report: the percentage changed, the coordinates did not.

## Details
- `sklearn/decomposition/truncated_svd.py`: use `axis=0` in `mean_variance_axis`.
- `doc/whats_new/v0.20.rst`: bug-fix entry.
- The existing `test_explained_variance` (sparse vs dense ratios) is the regression test.

## Verification
- Before: `pytest sklearn/decomposition/tests/test_truncated_svd.py` -> 1 failed, 14 passed (`Max relative difference: 0.08188466`).
- After: 15 passed; the class docstring doctest also passes.
