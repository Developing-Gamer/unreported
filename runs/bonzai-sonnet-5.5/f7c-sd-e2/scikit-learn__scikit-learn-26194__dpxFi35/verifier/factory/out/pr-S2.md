Fix l1_min_c intercept term for imbalanced multiclass data

`l1_min_c` computed the intercept contribution to its denominator as `abs(np.dot(Y, bias).max())`, taking the max before the absolute value. Y is the +1/-1 one-vs-rest label matrix, so each row's term is `intercept_scaling * (n_pos - n_neg)`. In an imbalanced multiclass problem with no majority class every row is negative, so `max` picks the smallest magnitude. The denominator came out too small and the lower bound for C too large (e.g. 8x for classes 45/45/10: 0.2 instead of 0.025 for log loss). Binary data has a single row, so it was unaffected.

The fix takes the absolute value first: `np.abs(np.dot(Y, bias)).max()`.

Verification: new regression test `test_l1_min_c_multiclass_imbalanced_intercept` (both losses) failed before the change (0.2 != 0.025) and passes after; all of `sklearn/svm/tests/test_bounds.py` passes (28 tests).

Run: `python -m pytest sklearn/svm/tests/test_bounds.py -q`
