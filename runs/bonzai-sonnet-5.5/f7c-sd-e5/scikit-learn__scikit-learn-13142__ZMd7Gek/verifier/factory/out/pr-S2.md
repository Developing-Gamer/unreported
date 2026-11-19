Fix TruncatedSVD explained_variance_ratio_ for sparse input

## Overview
For sparse input, `TruncatedSVD.fit_transform` divided the explained variance by the sum of per-sample (row) variances (`mean_variance_axis(X, axis=1)`), while the dense branch uses the per-feature total (`np.var(X, axis=0).sum()`). The percentage of explained variance was therefore wrong for sparse batches (unless n_samples == n_features), while `components_` and the embedding (`U * Sigma`) were unaffected, which matches the report ("percentage dropped, coordinates unchanged").

## Changes
- `sklearn/decomposition/truncated_svd.py`: use `axis=0` in `mean_variance_axis`.
- `sklearn/decomposition/tests/test_truncated_svd.py`: new test comparing sparse vs dense `explained_variance_ratio_` on tall (100x20) and wide (20x100) matrices, both solvers.
- `doc/whats_new/v0.20.rst`: changelog entry.

## Verification
- Before the fix: `pytest sklearn/decomposition/tests/test_truncated_svd.py -k explained_variance` -> 5 failed (new tests and the existing `test_explained_variance`, e.g. max relative difference 0.08).
- After the fix: whole `test_truncated_svd.py` -> 19 passed.
