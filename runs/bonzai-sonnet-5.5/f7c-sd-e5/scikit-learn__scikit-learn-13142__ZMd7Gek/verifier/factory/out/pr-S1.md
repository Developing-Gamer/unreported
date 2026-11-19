Fix GaussianMixture fit_predict labels disagreeing with predict when n_init > 1

## Overview
With `n_init > 1`, `fit_predict(X)` returned labels from the last initialization's parameters, while the model kept the best initialization's parameters. So `fit_predict(X)` and `predict(X)` often disagreed (81.5% mismatched in the regression test). This moves the final E-step after the best parameters are restored.

## Details
- `sklearn/mixture/base.py`: in `BaseMixture.fit_predict`, `_set_parameters(best_params)` now runs before the final `_e_step(X)` that yields the labels. Applies to `GaussianMixture` and `BayesianGaussianMixture`.
- Added `test_gaussian_mixture_fit_predict_n_init` and a changelog entry in `doc/whats_new/v0.20.rst`.

## Verification
- `python -m pytest sklearn/mixture/tests/test_gaussian_mixture.py -k fit_predict_n_init -q`: fails before the fix (815/1000 labels differ), passes after.
- `python -m pytest sklearn/mixture -q`: 57 passed.
