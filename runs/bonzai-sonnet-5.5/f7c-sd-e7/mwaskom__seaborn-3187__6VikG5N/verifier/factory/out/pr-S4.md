Fix RGBA colour arrays losing their own alpha in resolve_color

## Overview
In layered scatter charts the points looked opaque while their legend swatches stayed translucent. `resolve_color` returned a single RGBA colour unchanged (keeping its alpha), but for an N×4 RGBA array it called `to_rgba_array(color, alpha)`, which overwrites every colour's alpha with the mark's alpha (default 1). Plotted points resolve colours as arrays, so they became opaque; legend swatches resolve a single colour and kept the alpha.

## Details
- `seaborn/_marks/base.py`: the N×4 array branch now calls `mpl.colors.to_rgba_array(color)`, matching the scalar RGBA branch.
- `tests/_marks/test_base.py`: `test_color_rgba_array_keeps_alpha` checks that a 2-row RGBA array with alpha 0.4 and a default mark alpha keeps 0.4 on both rows, and equals the scalar path.

## Verification
- `python -m pytest tests/_marks/test_base.py -q`: new test fails before the change (alpha 1.0 vs 0.4), passes after.
- `python -m pytest tests/_marks tests/_core/test_plot.py -q`: 149 failures both before and after (pandas errors in this environment, unrelated); the pass count rises by one (the new test).
