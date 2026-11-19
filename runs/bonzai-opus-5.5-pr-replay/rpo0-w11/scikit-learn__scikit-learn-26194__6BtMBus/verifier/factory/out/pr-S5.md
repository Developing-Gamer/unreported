FIX roc_curve: use np.inf as the first threshold instead of max(y_score) + 1

## Overview
`roc_curve` prepends an extra threshold so the curve starts at (0, 0). It was set to `thresholds[0] + 1`, so with probability estimates in [0, 1] the first threshold landed in (1, 2], an impossible probability (e.g. 1.97 for `RandomState(42)` data). It is now `np.inf`, which still means "no instance predicted positive" and never lies inside the valid score range.

## Evidence
GitHub issue: "Thresholds can exceed 1 in `roc_curve` while providing probability estimate".

Before (base commit), new test fails:
`assert np.isinf(thresholds[0])` -> `AssertionError: assert False where False = isinf(1.9699098521619942)`

After: the test passes; `thresholds[0]` is `inf` and the rest are in [0, 1].

## Details
- `sklearn/metrics/_ranking.py`: `thresholds = np.r_[np.inf, thresholds]`; docstring and doctest output updated (`array([ inf, 0.8, 0.4, 0.35, 0.1])`).
- `sklearn/metrics/tests/test_ranking.py`: added `test_roc_curve_with_probablity_estimates`; `test_roc_curve_drop_intermediate` now expects `np.inf` first.
- `doc/whats_new/v1.3.rst`: Fix entry (the `:pr:` / author attribution still needs to be added once the PR number is known).
- Behaviour change: `thresholds[0]` is no longer finite. The `_plot` display code does not use thresholds, and `y_score >= inf` is False, so the tpr/fpr consistency is preserved.

## Verification
`pytest sklearn/metrics/_ranking.py sklearn/metrics/_plot/tests/test_roc_curve_display.py sklearn/metrics/tests/test_ranking.py --doctest-modules` -> 268 passed. `pytest sklearn/metrics -k "roc or ranking or det or public" --doctest-modules` -> 402 passed.
