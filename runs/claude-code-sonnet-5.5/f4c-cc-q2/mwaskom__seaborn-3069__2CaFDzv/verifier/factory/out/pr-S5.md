Do not stack KDE curves in histplot when multiple="stack"

Root cause: `_DistributionPlotter.plot_univariate_histogram` passed the density curves through `_resolve_multiple` for everything but "dodge". With "stack" the per-group KDEs were cumulatively summed, so the overlay no longer represented each group's density.

Change: skip resolution of the densities for "stack" as well as "dodge" (`seaborn/distributions.py`). "fill" is unchanged. Added a whatsnew entry.

Verification: new test `test_kde_with_hue_stack_matches_layer` checks that the stacked and layered KDE lines are identical; it fails before and passes after. The existing histplot/kdeplot tests still pass.
