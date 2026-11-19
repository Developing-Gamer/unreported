import numpy as np
from numpy.testing import assert_allclose
from sklearn.linear_model import BayesianRidge


def test_normalized_predictive_uncertainty_is_translation_invariant():
    rng = np.random.RandomState(20)
    X = rng.normal(size=(48, 3))
    y = X.dot(np.array([1.8, -0.7, 0.4])) + 0.3 * rng.normal(size=48)
    queries = rng.normal(size=(7, 3))
    shift = np.array([9.0, -5.0, 4.0])

    original = BayesianRidge(normalize=True).fit(X, y)
    translated = BayesianRidge(normalize=True).fit(X + shift, y)

    mean, std = original.predict(queries, return_std=True)
    translated_mean, translated_std = translated.predict(
        queries + shift, return_std=True
    )

    assert_allclose(translated_mean, mean, rtol=1e-9, atol=1e-11)
    assert_allclose(translated_std, std, rtol=1e-9, atol=1e-11)
