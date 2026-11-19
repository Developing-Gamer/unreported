import numpy as np
import pytest
from scipy import sparse

from sklearn.decomposition import TruncatedSVD


@pytest.mark.parametrize('matrix_type', [sparse.csr_matrix, sparse.csc_matrix])
def test_sparse_variance_ratio_matches_total_feature_variance(matrix_type):
    X = np.array([
        [4, 0, 0, 1, 0],
        [4, 2, 0, 0, 0],
        [4, 0, 3, 0, 0],
        [4, 0, 0, 0, 2],
        [4, 1, 0, 2, 0],
        [4, 0, 1, 0, 0],
        [4, 0, 0, 3, 1],
        [4, 2, 0, 0, 1],
    ], dtype=float)
    model = TruncatedSVD(n_components=2, algorithm='arpack', random_state=0)
    scores = model.fit_transform(matrix_type(X))

    total_feature_variance = np.var(X, axis=0).sum()
    expected_ratio = np.var(scores, axis=0) / total_feature_variance
    np.testing.assert_allclose(
        model.explained_variance_ratio_, expected_ratio,
        rtol=1e-10, atol=1e-12,
    )
