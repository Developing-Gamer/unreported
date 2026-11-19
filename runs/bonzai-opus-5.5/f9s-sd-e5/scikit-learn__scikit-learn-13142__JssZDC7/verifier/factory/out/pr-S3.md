Fix BayesianRidge.predict(return_std=True) inflating the std when features are not centred

## Overview
After the latest rollout, prediction interval widths for several regional models rose sharply while point forecasts and RMSE were unchanged. `BayesianRidge.predict(X, return_std=True)` computed the predictive std on uncentred features, so the std grew with the distance of the feature means from zero (std ~0.97 instead of ~0.1 in the regression test data).

## Cause
`sigma_` is estimated on data centred by `X_offset_` (fit_intercept) and scaled by `X_scale_` (normalize). `predict` only divided by `X_scale_` when `normalize=True` and never subtracted `X_offset_`, so `x^T Sigma x` was evaluated on the wrong coordinates. The mean prediction uses `coef_`/`intercept_`, so it was unaffected. The same applied to `normalize=False` with `fit_intercept=True`, which also centres in `fit`.

## Fix
`predict` now always uses `(X - X_offset_) / X_scale_` (offset is 0 and scale is 1 when the options are off), matching `ARDRegression.predict`. Added `test_bayesian_ridge_return_std_normalize` and a changelog entry.

Not changed: `ARDRegression.fit` does not store `X_offset_`/`X_scale_`, which is a separate issue.

## Verification
- New test fails before (std ~0.97 vs <0.2 expected) and passes after.
- `pytest sklearn/linear_model/tests/test_bayes.py`: 12 passed.
