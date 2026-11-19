Fix svm.l1_min_c overestimating C for imbalanced multiclass targets

## Overview
With `fit_intercept=True`, `l1_min_c` computed the intercept term as `abs(np.dot(Y, bias).max())`, i.e. the absolute value of the largest *signed* class sum. For imbalanced multiclass labels, minority classes have large negative one-vs-rest sums that were ignored, so the denominator was too small and the returned minimum `C` too large (e.g. 3x for the 3-class case below). Binary targets have a single row in `Y`, so they were unaffected.

## Details
- `sklearn/svm/_bounds.py`: use `np.max(np.abs(np.dot(Y, bias)))` (abs before max).
- `sklearn/svm/tests/test_bounds.py`: new regression test with `y = [0]*6 + [1]*2 + [2]*2` and an all-zero `X`; class sums are 2, -6, -6, so `C` must be `0.5/6` (squared hinge) or `2/6` (log). Before the fix it returned `0.5/2` / `2/2`.
- `doc/whats_new/v1.3.rst`: changelog entry.

## Verification
`python -m pytest sklearn/svm/tests/test_bounds.py`: before the fix 6 failed (the 2 new tests plus 4 existing fit-intercept multi-class cases), after the fix 28 passed.
