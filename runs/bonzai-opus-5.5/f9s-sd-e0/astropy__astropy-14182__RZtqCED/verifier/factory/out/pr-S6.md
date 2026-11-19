Raise ValueError from squeeze() when the axis cannot be squeezed

## Overview
`Time`, `SkyCoord`, representations and other `ShapedLikeNDArray` classes silently returned the original, still multi-dimensional object from `squeeze(axis=...)` when the axis length was not 1. numpy raises `ValueError` in that case. Callers that rely on squeeze to normalise dimensions got an unchanged 2-D object and failed much later. `squeeze` now raises immediately, as `numpy.ndarray.squeeze` does.

## Details
- `NDArrayShapeMethods.squeeze` (astropy/utils/shapes.py) wrapped `_apply("squeeze", ...)` in `try/except ValueError: return self`. Removed; the error from numpy now propagates.
- Regression test `test_squeeze_invalid_axis_raises` in astropy/utils/tests/test_shapes.py: shape (5, 2) `Time` raises on `squeeze(axis=1)`; shape (5, 1) still squeezes to (5,).
- Changelog: docs/changes/utils/14200.bugfix.rst.
- Behaviour change: code that relied on the silent pass-through now gets a ValueError (same as numpy).

## Verification
- `python -m pytest astropy/utils/tests/test_shapes.py -k squeeze`: failed before the fix (DID NOT RAISE ValueError), passes after.
- Existing squeeze tests in time/coordinates (test_methods, test_shape_manipulation, test_representation_methods) pass; remaining failures are pre-existing/unrelated (leap-second auto-update needs network; numpy-version failures in test_quantity_non_ufuncs, identical on base).
