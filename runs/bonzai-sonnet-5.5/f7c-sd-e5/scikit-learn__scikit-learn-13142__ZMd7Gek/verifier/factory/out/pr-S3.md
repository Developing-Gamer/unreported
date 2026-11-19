Fix BayesianRidge/ARDRegression return_std growing with the feature mean

## Overview
`predict(X, return_std=True)` in `BayesianRidge` and `ARDRegression` computes the variance from a posterior covariance fitted on centred (and optionally scaled) features, but the query rows were never centred. The predictive std therefore grew with the feature mean while point predictions stayed the same, which widens prediction intervals sharply for un-centred features. `ARDRegression` also never stored `X_offset_`/`X_scale_`, so `normalize=True` raised `AttributeError`.

## Details
- `BayesianRidge.predict` and `ARDRegression.predict` now use `(X - X_offset_) / X_scale_` before computing the variance (for ARD, before applying the `lambda_ < threshold_lambda` column mask).
- `ARDRegression.fit` stores `X_offset_` and `X_scale_`.
- New test `test_return_std_with_large_feature_offset`: features shifted by +1000 must give the same mean/std as unshifted features, for both estimators and `normalize` on/off. Before the fix std was ~86.7 vs ~0.11; after, they match.
- whats_new entry added.

## Verification
`/opt/miniconda3/envs/testbed/bin/python -m pytest sklearn/linear_model/tests/test_bayes.py -q` — 12 passed (new test failed before the fix).
