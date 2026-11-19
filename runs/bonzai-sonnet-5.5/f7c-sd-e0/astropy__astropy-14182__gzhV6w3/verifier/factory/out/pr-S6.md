Stop ShapedLikeNDArray.squeeze from swallowing ValueError

## Overview
`ShapedLikeNDArray.squeeze` (used by `Time`, `SkyCoord`, frames, representations) caught `ValueError` and returned `self`. So `squeeze(axis=k)` on an axis whose length is not 1 returned the still multi-dimensional object instead of raising like numpy, and failures only showed up later, far from the mistake. The `try/except` is removed so the error propagates.

## Details
- `astropy/utils/shapes.py`: `squeeze` now just returns `self._apply("squeeze", ...)`.
- Tests: `Time.squeeze(axis=<non-unit axis>)` and `SkyCoord.squeeze(axis=<non-unit axis>)` raise `ValueError`; squeezing a unit axis still works. Existing `squeeze()` tests are unchanged and pass.
- Changelog: `docs/changes/utils/14000.bugfix.rst`.

## Verification
- Before: `pytest astropy/time/tests/test_methods.py -k squeeze` fails with "DID NOT RAISE ValueError".
- After: passes. Related time/coordinates/shape test files pass, except `TestArithmetic::test_ptp[masked]`, which fails on an expired leap-second file/network warning, unrelated to this change.
