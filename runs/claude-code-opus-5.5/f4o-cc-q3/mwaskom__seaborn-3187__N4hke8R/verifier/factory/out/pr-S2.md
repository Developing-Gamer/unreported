Fix Dodge(gap=...) so dodged marks are actually separated

## Root cause
`Dodge.__call__` multiplied the dodged widths by `1 - gap` *before* turning them into offsets. The offsets were then calculated from the narrowed widths, so the thinner marks were packed edge to edge again. Increasing `gap` made grouped bars thinner, but bars in the same group still touched.

## Change
`seaborn/_core/moves.py`: compute the offsets from the full dodged widths first, then apply the `1 - gap` shrink to the widths only. Each mark keeps its dodged center and gets narrower, which leaves real space between neighbors.

## Verification
- The existing `tests/_core/test_moves.py::TestDodge::test_gap` already encoded the correct behavior and was failing on this checkout. It passes now.
- Added `TestDodge::test_widths_gap`, which covers unequal widths. It fails before the change and passes after.
- The full `tests/_core` and `tests/_marks` suites pass.
