from sympy import Rational, pi
from sympy.physics.optics import refraction_angle


def test_scalar_total_internal_reflection_is_rejected():
    error = None
    try:
        refraction_angle(pi/3, Rational(3, 2), 1)
    except ValueError as exc:
        error = exc

    assert error is not None, 'Total internal reflection must not produce a transmitted angle'
    assert 'total internal reflection' in str(error)
