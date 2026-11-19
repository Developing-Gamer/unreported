Fix Bezier/closed-path intersection tolerance being compared as a squared distance

## Overview
Connectors clipped to circular node borders could stop up to ~0.05 display units short of the border, leaving hairline gaps in vector exports (visible when zooming in). `find_bezier_t_intersecting_with_closedpath` documents `tolerance` as a distance, but compared the squared distance to it, so the default 0.01 effectively meant ~0.1.

## Details
- `lib/matplotlib/bezier.py`: terminate the bisection when `np.hypot(dx, dy) < tolerance`. `split_path_inout` (used by `ConnectionStyle._clip`/`_shrink`) inherits the fix; `patches.py` needs no change.
- New `lib/matplotlib/tests/test_bezier.py`: checks the bracketing points are closer than `tolerance` (was 0.078 vs 0.01) and that `split_path_inout` ends on the circle border.

## Verification
- `python -m pytest lib/matplotlib/tests/test_bezier.py`: the distance test fails before (0.078125 < 0.01) and passes after.
- `test_bezier.py test_patches.py test_arrow_patches.py test_text.py test_path.py`: 217 passed, 19 skipped.
- `test_axes.py::test_canonical[pdf]` etc. fail in this working tree with or without this change (caused by unrelated uncommitted PDF text-measurement changes already present), not by this fix.
