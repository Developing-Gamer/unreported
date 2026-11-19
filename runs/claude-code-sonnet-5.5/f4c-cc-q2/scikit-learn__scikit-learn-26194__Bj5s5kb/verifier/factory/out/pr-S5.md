Fix roc_curve returning a first threshold greater than 1 for probability scores

## Root cause
`roc_curve` adds an extra point so the curve starts at (0, 0), using `thresholds[0] + 1` as its threshold. When `y_score` is a probability estimate this yields a threshold above 1, which is not a meaningful probability cut-off.

## Change
The extra threshold is now `np.inf` (no instance is predicted positive), in `sklearn/metrics/_ranking.py`. The docstring, the doctest and `doc/modules/model_evaluation.rst` are updated, and a changelog entry is added. Callers that relied on `max(y_score) + 1` as the first threshold now get `inf`.

## Verification
- Added `test_roc_curve_with_probablity_estimates`.
- Updated the expected thresholds in `test_roc_curve_drop_intermediate`.
- Ran `pytest sklearn/metrics sklearn/feature_selection sklearn/tests/test_public_functions.py`; all pass.
- The doctests in `_ranking.py` and `model_evaluation.rst` pass.
