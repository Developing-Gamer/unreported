Fix GaussianMixture.fit_predict labels disagreeing with predict when n_init > 1

## Overview
With `n_init > 1`, `fit_predict(X)` returned labels computed from the last initialization's parameters, while the model kept the parameters of the best initialization. So `fit_predict(X)` and `predict(X)` often disagreed (e.g. 815/1000 labels differed on `randn(1000, 5)`, n_components=5, n_init=5).

## Details
In `BaseMixture.fit_predict` the final E-step ran before `_set_parameters(best_params)`. The final E-step now runs after the best parameters are restored. Added `test_gaussian_mixture_fit_predict_n_init` and a changelog entry in `doc/whats_new/v0.20.rst`.

## Proof
- Before: the new test fails with `AssertionError: Arrays are not equal ... Mismatched elements: 815 / 1000 (81.5%)`.
- After: it passes; `pytest sklearn/mixture` gives 57 passed.

## Verification
`python -m pytest sklearn/mixture -q` (57 passed).
