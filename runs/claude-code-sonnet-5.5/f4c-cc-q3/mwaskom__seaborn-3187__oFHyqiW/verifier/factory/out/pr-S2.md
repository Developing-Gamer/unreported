Fix Dodge(gap=...) leaving dodged marks touching

Root cause: In `Dodge.__call__`, widths were shrunk by `1 - gap` before the dodge offsets were computed from them, so the centers moved closer together by the same factor and bars within a group still touched (reported in S2).

Change: compute offsets from the unshrunk widths, then apply the gap to the widths (`seaborn/_core/moves.py`).

Verification: the existing `TestDodge::test_gap` (expected x = [-.2, .2, 1.2], width .3) failed before the change and passes now; tests/_core/test_moves.py and tests/_core/test_plot.py pass.
