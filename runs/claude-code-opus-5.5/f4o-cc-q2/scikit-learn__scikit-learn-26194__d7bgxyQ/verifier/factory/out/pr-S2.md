Fix l1_min_c overestimating C for imbalanced multiclass targets when fit_intercept=True

## Root cause
`sklearn.svm.l1_min_c` computes the denominator as the largest absolute value of `Y @ X`, and of `Y @ bias` when an intercept is fitted. `Y` is the ±1 label-binarized target with one row per class. The intercept term used `abs(np.dot(Y, bias).max())`, which takes the *signed* maximum first and then the absolute value. With imbalanced multiclass targets, every class makes up less than half of the samples, so every entry of `Y @ bias` is negative. The signed max is then the entry with the *smallest* magnitude, which underestimates the denominator and makes the returned minimum C too large. For example, `y = [0]*4 + [1]*3 + [2]*3` gives `[-2, -4, -4]`: the old code used 2 instead of 4, so C was 2× too high, and more skewed class mixes give larger factors. Binary targets binarize to a single row, so the max is that row's value and the result was unchanged. This matches the production report (S2): three-class runs start the C grid ~4× higher, binary runs unchanged.

## Change
- `sklearn/svm/_bounds.py`: `abs(np.dot(Y, bias).max())` → `abs(np.dot(Y, bias)).max()`.
- Changelog entry in `doc/whats_new/v1.3.rst`.

## Verification
- New test `sklearn/svm/tests/test_bounds.py::test_l1_min_c_multiclass_intercept_imbalanced` checks exact values for both losses. It fails on the old code and passes with the fix.
- `pytest sklearn/svm sklearn/linear_model/tests/test_logistic.py` all pass.
