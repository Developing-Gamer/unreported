Fix Bezier/closed-path intersection stopping on squared distance instead of distance

## Overview
Connectors clipped or shrunk at circular node borders could end slightly short of (or past) the border, by a different amount per connector. This is visible as tiny gaps when zooming into SVG/PDF exports. `find_bezier_t_intersecting_with_closedpath` documented `tolerance` as a distance but compared the squared distance to it, so with the default 0.01 the bisection stopped at a bracket of ~0.1 units instead of 0.01.

## Details
- `lib/matplotlib/bezier.py`: stop test is now `np.hypot(dx, dy) < tolerance`, matching the docstring.
- `lib/matplotlib/tests/test_bezier.py`: new test; a segment (0,0)-(100,0) against `inside_circle(0, 0, 37.3)` with `tolerance=0.01` must give a bracket narrower than 0.01 and a midpoint within 0.01 of the radius. Before the fix it fails with `assert (37.3046875 - 37.20703125) < 0.01`.
- Callers (`ConnectionStyle._Base._clip/_shrink` via `split_path_inout`) are unchanged; they simply become more precise. Existing arrow image comparisons (7 failing on the base) now pass.

## Verification
- `python -m pytest lib/matplotlib/tests/test_bezier.py` fails on base, passes with fix.
- `python -m pytest lib/matplotlib/tests/test_bezier.py lib/matplotlib/tests/test_arrow_patches.py lib/matplotlib/tests/test_patches.py lib/matplotlib/tests/test_path.py`: 138 passed, 11 skipped (base: 7 failed in arrow/patches tests).
