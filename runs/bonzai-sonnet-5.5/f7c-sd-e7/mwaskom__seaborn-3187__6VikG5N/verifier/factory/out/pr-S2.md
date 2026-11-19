Fix Dodge gap so it separates dodged marks instead of only narrowing them

## Overview
With `Dodge(gap=...)`, increasing the gap made grouped bars thinner but the bars within a group still touched. `Dodge` shrank the widths by `(1 - gap)` before computing offsets, so the offsets were laid out edge to edge from the already-narrowed widths. Offsets are now computed from the full-width slots and the marks are narrowed afterwards, so the gap shows up as space between marks.

## Details
- `seaborn/_core/moves.py`: in `Dodge.__call__`, compute `offsets` before applying `new_widths *= 1 - self.gap`.
- Example: two bars of width .8 with `gap=.25` now have centres at ±.2 and width .3, leaving .1 between them (previously centres ±.15, touching).
- Existing `tests/_core/test_moves.py::TestDodge::test_gap` already encodes this behaviour; it failed before the change (x was [-.15, .15, 1.15] instead of [-.2, .2, 1.2]) and passes now.

## Verification
- `pytest tests/_core/test_moves.py::TestDodge::test_gap` failed before, passes after.
- `pytest tests/_core/test_moves.py tests/_core/test_plot.py`: 207 passed, 5 xfailed.
