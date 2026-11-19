from sympy import Symbol
from sympy.polys.orthopolys import laguerre_poly


def test_laguerre_parameter_validation():
    x = Symbol('x')
    assert laguerre_poly(2, x) == x**2/2 - 2*x + 1
    assert laguerre_poly(2, x, alpha=2) == x**2/2 - 4*x + 6

    rejected = False
    try:
        laguerre_poly(2, x, alpha=object())
    except (TypeError, ValueError):
        rejected = True

    assert rejected, 'An invalid parameter must not silently select the default basis'
