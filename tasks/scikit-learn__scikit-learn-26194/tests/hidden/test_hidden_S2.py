import numpy as np
import pytest
from scipy.sparse import csc_matrix

from sklearn.svm import l1_min_c


@pytest.mark.parametrize("sparse_input", [False, True])
@pytest.mark.parametrize("loss, numerator", [("squared_hinge", 0.5), ("log", 2.0)])
def test_multiclass_intercept_bound_uses_largest_absolute_class_total(
    sparse_input, loss, numerator
):
    y = np.repeat(np.arange(3), [6, 3, 1])
    X = np.full((10, 1), 0.1)
    if sparse_input:
        X = csc_matrix(X)

    actual = l1_min_c(X, y, loss=loss, fit_intercept=True)

    # Signed class totals are 2, -4, and -8. Their largest absolute
    # value is 8, exceeding every feature contribution (at most 0.8).
    assert actual == pytest.approx(numerator / 8.0)
