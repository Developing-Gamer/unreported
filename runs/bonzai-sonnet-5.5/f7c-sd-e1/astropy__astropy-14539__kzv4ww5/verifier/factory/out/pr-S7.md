Raise for an invalid max_radius in uniform_spherical_random_volume instead of returning unitless radii

## Overview
`uniform_spherical_random_volume` wrapped `u.Quantity(max_radius)` in `try/except ValueError` and fell back to a dimensionless `1`. A `max_radius` such as `"10 kpcs"` (unparseable unit) therefore produced unitless radii, all below 1, with no error. A mock catalog export hit this: the job succeeded but the radius column lost its kpc unit. The function now raises the `ValueError`.

## Evidence
Support report: "The latest mock catalog job completed successfully, but its radius column is unitless and every value is below 1. Previous exports had distances in kpc."

## Before / after
- Before: `uniform_spherical_random_volume(size=3, max_radius="10 kpcs")` returned a dimensionless distance. The new test fails with `Failed: DID NOT RAISE <class 'ValueError'>`.
- After: it raises `ValueError`. `max_radius="10 kpc"` gives distances in kpc, at most 10.

## Details
- Removed the try/except in `astropy/coordinates/angle_utilities.py`. A bad value is now reported where it is passed, not hidden.
- Tests added in `astropy/coordinates/tests/test_angle_generators.py` for the invalid string and for a valid string.
- Changelog: `docs/changes/coordinates/14600.bugfix.rst`. The number is a placeholder, so rename it to the real PR number.

## Verification
`python -m pytest astropy/coordinates/tests/test_angle_generators.py astropy/coordinates/tests/test_angles.py`: 101 passed.
