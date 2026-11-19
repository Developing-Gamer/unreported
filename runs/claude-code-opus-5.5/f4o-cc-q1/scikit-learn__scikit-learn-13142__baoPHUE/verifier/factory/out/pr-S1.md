Fix GaussianMixture/BayesianGaussianMixture fit_predict disagreeing with predict when n_init > 1

## Root cause
`BaseMixture.fit_predict` (`sklearn/mixture/base.py`) runs one last E-step to compute the labels it returns. That E-step ran *before* `self._set_parameters(best_params)`. So it used the parameters from the **last** initialization, not the one with the best lower bound. With `n_init=1` the two are the same, which is why the existing `test_gaussian_mixture_fit_predict` didn't catch this. With `n_init > 1`, `fit_predict(X)` returned labels from one model while the fitted estimator (and so `predict(X)`) held another.

## Change
- Moved the final `_e_step(X)` in `BaseMixture.fit_predict` to after `_set_parameters(best_params)`, `n_iter_` and `lower_bound_` are set. The returned labels now come from the selected model. This applies to both `GaussianMixture` and `BayesianGaussianMixture`.
- Added the regression tests `test_gaussian_mixture_fit_predict_n_init` and `test_bayesian_mixture_fit_predict_n_init`. They check that `fit_predict(X)` equals `predict(X)` with `n_init > 1`.

## Verification
- Without the fix, both new tests fail with mismatched label arrays. With the fix, both pass.
- `pytest sklearn/mixture`: 58 passed.
