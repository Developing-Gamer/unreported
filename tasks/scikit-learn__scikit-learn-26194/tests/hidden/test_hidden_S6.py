import numpy as np
import pytest
from scipy import sparse

from sklearn.feature_selection import VarianceThreshold


@pytest.mark.parametrize("use_sparse", [False, True])
def test_variance_threshold_uses_population_variance(use_sparse):
    X = np.array([[0, 0], [0, 2], [0, 0], [1, 2]], dtype=float)
    data = sparse.csr_matrix(X) if use_sparse else X

    selector = VarianceThreshold(threshold=0.2).fit(data)

    np.testing.assert_array_equal(selector.get_support(), [False, True])
    np.testing.assert_allclose(selector.variances_, [0.1875, 1.0])
    transformed = selector.transform(data)
    if sparse.issparse(transformed):
        transformed = transformed.toarray()
    np.testing.assert_array_equal(transformed, X[:, [1]])
