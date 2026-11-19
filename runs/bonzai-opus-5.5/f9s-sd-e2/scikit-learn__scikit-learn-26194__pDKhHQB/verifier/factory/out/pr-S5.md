FIX roc_curve: use np.inf for the first threshold instead of max(y_score) + 1

## Overview
`roc_curve` prepends an extra threshold so the curve starts at (0, 0). It was set to `thresholds[0] + 1`, so with probability estimates in [0, 1] the first threshold landed in (1, 2], outside the valid probability range (reported in the GitHub issue "Thresholds can exceed 1 in `roc_curve` while providing probability estimate"). The first threshold is now `np.inf`, which correctly means "no instance predicted positive" for any score scale.

## Details
- `sklearn/metrics/_ranking.py`: `thresholds = np.r_[np.inf, thresholds]`; docstring and doctest updated.
- `doc/modules/model_evaluation.rst`: doctest output updated.
- `sklearn/metrics/tests/test_ranking.py`: new non-regression test `test_roc_curve_with_probablity_estimates`; `test_roc_curve_drop_intermediate` now expects `np.inf` first.
- `doc/whats_new/v1.3.rst`: changelog entry (Fix).

Behaviour change: `thresholds[0]` is `inf` rather than `max(y_score) + 1`.

## Proof
Before: new test fails on the base commit with `assert np.isinf(thresholds[0])` -> `isinf(1.9699...)` False.
After: passes.

## Verification
- `python -m pytest sklearn/metrics/tests/test_ranking.py -k roc_curve_with_probablity -q`
- `python -m pytest sklearn/metrics sklearn/tests/test_public_functions.py -q` (3061 passed)
- `python -m pytest --doctest-modules sklearn/metrics/_ranking.py` and doctest of `doc/modules/model_evaluation.rst` pass.
