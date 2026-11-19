from sympy import Rational, exp, pi, simplify, sqrt
from sympy.stats import Bernoulli, Normal, density


def test_normal_with_bernoulli_mean_density():
    mean = Bernoulli('mean', Rational(1, 4))
    observation = Normal('observation', mean, 1)

    actual = density(observation)(0)
    expected = (Rational(3, 4) + exp(-Rational(1, 2)) / 4) / sqrt(2*pi)

    assert simplify(actual - expected) == 0
