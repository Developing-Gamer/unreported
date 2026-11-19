Use np.inf as the leading threshold in roc_curve so thresholds do not exceed 1 for probability estimates

## Root cause
`roc_curve` prepends an extra threshold so that the curve starts at (fpr, tpr) = (0, 0). That threshold was `thresholds[0] + 1`, i.e. `max(y_score) + 1`. When `y_score` is a probability estimate this gives a value above 1 (e.g. 1.97), which makes no sense for probabilities. Clipping it to 1 would also be wrong, because a score equal to 1 would then be predicted positive at the "no positives" point.

## Change
- `sklearn/metrics/_ranking.py`: `thresholds = np.r_[np.inf, thresholds]`. Also updated the docstring text and the docstring example.
- Updated the `roc_curve` example in `doc/modules/model_evaluation.rst`.
- Updated the expected values in `test_roc_curve_drop_intermediate`, which had hard-coded the old `2.0` sentinel.
- Changelog entry in `doc/whats_new/v1.3.rst`. This is a small behaviour change: `thresholds[0]` is now `inf`.

## Verification
- New test `test_roc_curve_with_probablity_estimates` (uses the `global_random_seed` fixture) asserts that `thresholds[0]` is inf and that every other threshold is in [0, 1]. The reproducer from the issue gave 1.97 before the fix.
- `pytest sklearn/metrics` (including `_plot`) passes, and the doctests in `_ranking.py` and `model_evaluation.rst` pass.
