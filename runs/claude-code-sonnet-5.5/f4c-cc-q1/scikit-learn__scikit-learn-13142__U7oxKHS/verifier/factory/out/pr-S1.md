Fix GaussianMixture.fit_predict disagreeing with predict when n_init > 1

Root cause: in `BaseMixture.fit_predict` the final E-step (used to compute returned labels) ran before `_set_parameters(best_params)`. With n_init > 1 the model's parameters at that point were from the last initialization, not the best one, so labels differed from `fit(X).predict(X)`.

Change: move the final E-step after `_set_parameters(best_params)` in `sklearn/mixture/base.py`. Test `test_gaussian_mixture_fit_predict` now uses `n_init=3`.

Verification: the updated test fails before the fix and passes after; `pytest sklearn/mixture` passes.
