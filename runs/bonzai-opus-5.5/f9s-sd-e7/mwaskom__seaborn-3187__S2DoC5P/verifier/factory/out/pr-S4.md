Fix RGBA colours losing their own alpha for plotted marks while legends keep it

## Overview
Points in layered scatter charts with a colour that carries its own alpha (e.g. `(1, 0, 0, .3)`) rendered opaque, while their legend swatches stayed translucent. `resolve_color` handled the two paths differently: single colours (legend artists) kept their alpha, but 2-D RGBA arrays (plotted data) had it replaced by the mark's `alpha` (default 1).

## Details
- `seaborn/_marks/base.py`: in `resolve_color`, the 2-D RGBA branch now calls `mpl.colors.to_rgba_array(color)` without the `alpha` argument, matching the single-colour branch.
- Test: `tests/_marks/test_base.py::TestMappable::test_color_with_own_alpha` (single and DataFrame-array inputs).

## Verification
- `python -m pytest tests/_marks/test_base.py -k own_alpha -q`: fails before (alpha 1.0 vs 0.3), passes after.
- `python -m pytest tests/_marks -q`: 72 failures (pandas-version errors) occur identically on the base commit; 12 pass.
