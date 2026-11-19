from sympy import Symbol, apart, sin
from sympy.polys.polyerrors import PolynomialError


def test_nonpolynomial_denominator_reports_unsupported_input():
    x = Symbol('x')
    expr = 1/(x + sin(x))
    error = None

    try:
        apart(expr, x)
    except PolynomialError as exc:
        error = exc

    assert error is not None, 'Unsupported input was silently accepted'
