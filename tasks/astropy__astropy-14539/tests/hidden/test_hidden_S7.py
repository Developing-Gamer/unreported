from astropy.coordinates.angle_utilities import uniform_spherical_random_volume


def test_invalid_radius_unit_is_rejected():
    rejected = False
    try:
        uniform_spherical_random_volume(size=4, max_radius="10 kiloparsecc")
    except ValueError:
        rejected = True

    assert rejected, "An unrecognized radius unit must raise rather than silently use a default"
