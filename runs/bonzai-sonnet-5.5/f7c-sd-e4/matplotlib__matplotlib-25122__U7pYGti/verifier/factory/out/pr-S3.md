Axis.clear(): keep axes.labelsize/labelweight/labelcolor for axis labels

## Overview
Plots created with `axes.labelsize`, `axes.labelweight` or `axes.labelcolor` set through rcParams or a style file came out with default-looking axis labels (size from `font.size`, normal weight, `text.color`). Labels styled per call (`set_xlabel(..., fontsize=...)`) were unaffected, which is why only scripts relying on rc/style settings looked wrong.

## Details
`Axis.__init__` builds the label with the `axes.label*` rcParams, then calls `Axis.clear()`. `clear()` calls `self.label._reset_visual_defaults()`, which resets color to `text.color` and the font to the default font properties, and never reapplies the `axes.label*` values. So every new Axes (and every `ax.cla()`) lost them. The fix reapplies color, fontsize and fontweight from `axes.labelcolor`, `axes.labelsize` and `axes.labelweight` right after the reset in `Axis.clear()`.

Regression test: `test_axis_label_rcparams_after_clear` in `lib/matplotlib/tests/test_axes.py` (fresh Axes, and after `ax.cla()`).

## Verification
- New test fails on the base commit (`assert 12.0 == 19`) and passes with the fix.
- Ran test_axes, test_text, test_style, test_ticker, test_polar and test_rcparams: 1599 passed. test_hist2d[pdf], test_hist2d_transpose[pdf] and test_mathtext_ticks fail the same way on the base commit (environment). Two test_rcparams warning tests failed only because I ran with `-W ignore::DeprecationWarning` to work around an old setuptools `pkg_resources` warning.
