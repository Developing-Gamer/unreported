Fix GaussianMixture/BayesianGaussianMixture fit_predict disagreeing with predict when n_init > 1

## Overview
With `n_init > 1`, `fit_predict(X)` returned labels that often differed from `predict(X)` on the same fitted estimator (815/1000 labels mismatched in a probe with `n_init=5`). `BaseMixture.fit_predict` ran its final E-step before restoring the best parameters, so the labels came from the last initialization rather than the best one.

## Evidence
GitHub issue: "GaussianMixture predict and fit_predict disagree when n_init>1". `fit(X).predict(X)` was unaffected because `fit` discards the labels from `fit_predict`.

## Details
- `sklearn/mixture/base.py`: in `fit_predict`, moved the final `self._e_step(X)` after `self._set_parameters(best_params)` (and the `n_iter_`/`lower_bound_` assignments). Labels now come from the same parameters `predict` uses.
- Added regression tests `test_gaussian_mixture_fit_predict_n_init` and `test_bayesian_mixture_fit_predict_n_init`. The existing fit_predict tests never set `n_init > 1`, so they missed this.
- Changelog entry in `doc/whats_new/v0.20.rst`.

## Verification
- `python -m pytest sklearn/mixture/tests/test_gaussian_mixture.py -k fit_predict_n_init`: fails before the fix (`Mismatched elements: 815 / 1000`), passes after.
- `python -m pytest sklearn/mixture -q`: 58 passed. Both new tests fail with `base.py` reverted.
