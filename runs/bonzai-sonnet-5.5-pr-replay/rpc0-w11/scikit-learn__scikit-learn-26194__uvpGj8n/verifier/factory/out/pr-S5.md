roc_curve: use np.inf as the first threshold instead of max(y_score) + 1

## Overview
`roc_curve` prepends an extra threshold so the curve starts at (0, 0). It was set to `thresholds[0] + 1`, i.e. `max(y_score) + 1`. For probability estimates this is always above 1 (e.g. 1.8 for a top score of 0.8), which is outside the range of the scores and misleading. The first threshold is now `np.inf`, which correctly means "no instance is predicted positive" and keeps all other thresholds within the score range.

## Details
- `sklearn/metrics/_ranking.py`: `thresholds = np.r_[np.inf, thresholds]`; docstring (with a `versionchanged` note) and example output updated.
- `doc/modules/model_evaluation.rst`: doctest output updated to `array([ inf, 0.8 , 0.4 , 0.35, 0.1 ])`.
- `sklearn/metrics/tests/test_ranking.py`: new `test_roc_curve_with_probablity_estimates` (fails before the fix: first threshold 1.96 != inf); `test_roc_curve_drop_intermediate` expectations updated from `2.0` to `np.inf`.
- `doc/whats_new/v1.3.rst`: changelog entry (PR number / author to be added).
- Risk: code that uses `thresholds[0]` as a finite number would now see `inf`; no such use in the repository (RocCurveDisplay does not use thresholds).

## Verification
- Before: `pytest sklearn/metrics/tests/test_ranking.py -k probablity_estimates` fails with `assert 1.9699098521619942 == inf`.
- After: passes; `pytest sklearn/metrics` -> 2904 passed; doctests of `_ranking.py` and `model_evaluation.rst` pass.
