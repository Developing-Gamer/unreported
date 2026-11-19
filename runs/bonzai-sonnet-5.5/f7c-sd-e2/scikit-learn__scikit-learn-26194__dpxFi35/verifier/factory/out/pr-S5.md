FIX roc_curve: use np.inf as first threshold so thresholds do not exceed 1 for probability scores

## Overview
`roc_curve` prepends an extra threshold so the curve starts at (0, 0). It was set to `max(y_score) + 1`, so for probability estimates the first threshold was always above 1 (e.g. 1.8 for a top score of 0.8). It is now `np.inf`, which means "no instance predicted positive" and stays outside any score range without looking like a valid probability.

## Evidence
GitHub issue "Thresholds can exceed 1 in `roc_curve` while providing probability estimate".

Before the fix, the new test fails: `assert np.isinf(thresholds[0])` -> `where False = <ufunc 'isinf'>(1.9699098521619942)`.

## Details
- `sklearn/metrics/_ranking.py`: `thresholds = np.r_[np.inf, thresholds]`; docstring and doctest updated (`array([ inf, 0.8 , 0.4 , 0.35, 0.1 ])`).
- `doc/modules/model_evaluation.rst`: same example output updated.
- `sklearn/metrics/tests/test_ranking.py`: new `test_roc_curve_with_probablity_estimates` (first threshold is inf, the rest within [0, 1]); `test_roc_curve_drop_intermediate` expectations changed from `2.0` to `np.inf`.
- `doc/whats_new/v1.3.rst`: changelog entry (the PR number and author in the entry are placeholders to be adjusted when the PR is opened).
- `RocCurveDisplay` does not use the thresholds, so it is unaffected.

Behaviour change: `thresholds[0]` is now `inf` instead of `max(y_score) + 1`. Code that used it as a finite number would need adapting.

## Verification
- `python -m pytest sklearn/metrics/tests/test_ranking.py -q -k roc_curve`: 2 failed, 16 passed before the fix (the new test and `test_roc_curve_drop_intermediate` with the updated `np.inf` expectation); 18 passed after.
- `python -m pytest sklearn/metrics sklearn/tests/test_public_functions.py -q`: 3061 passed, 57 skipped, 10 xfailed.
- `python -m pytest --doctest-modules sklearn/metrics/_ranking.py doc/modules/model_evaluation.rst`: 11 passed.
