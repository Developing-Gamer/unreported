Fix Dodge gap so dodged bars within a group no longer touch

## Overview
With `so.Dodge(gap=...)`, increasing the gap made grouped bars thinner but they still touched each other. The gap was applied to the widths before the per-bar offsets were computed, so the bars were re-packed edge to edge around the group center. Offsets are now computed from the ungapped widths and the gap is applied only to the drawn width, leaving real space between bars.

## Details
- `seaborn/_core/moves.py`: in `Dodge.__call__`, compute `offsets` before `new_widths *= 1 - self.gap`.
- Example: `Dodge(gap=.25)` on two bars at x=0 with width .8 gives centers -0.2/0.2 and width 0.3, so a 0.1 gap between them (previously centers -0.15/0.15, no gap).
- The existing `tests/_core/test_moves.py::TestDodge::test_gap` already asserts this and failed before the fix (ACTUAL `[-0.15, 0.15, 1.15]`, DESIRED `[-0.2, 0.2, 1.2]`).

## Verification
- `python -m pytest tests/_core/test_moves.py -k Dodge`: test_gap failed before, passes after.
- `python -m pytest tests/_core/test_moves.py`: 34 passed.
