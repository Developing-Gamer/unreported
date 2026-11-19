Fix GaussianMixture/BayesianGaussianMixture fit_predict disagreeing with predict when n_init > 1

## Overview
With `n_init > 1`, `fit_predict(X)` returned labels that often disagreed with `predict(X)` called right after (815/1000 labels differed in the probe with `n_init=5`). `fit(X).predict(X)` was correct because `fit` discards the labels.

## Cause
In `BaseMixture.fit_predict` the final E-step that produces the returned labels ran before `self._set_parameters(best_params)`, so labels came from the last initialization's parameters, not the best one that `predict` uses.

## Fix
Move the final E-step to after the best parameters are restored. Added a regression test (`test_gaussian_mixture_fit_predict_n_init`) and a changelog entry.

## Verification
- New test fails before (815 / 1000 mismatched) and passes after.
- `pytest sklearn/mixture/tests`: 57 passed.
