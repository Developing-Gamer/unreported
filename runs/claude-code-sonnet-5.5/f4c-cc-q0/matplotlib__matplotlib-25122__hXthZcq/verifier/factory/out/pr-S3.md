Respect axes.labelsize/labelcolor/labelweight rcParams for axis labels

Root cause: `Axis.__init__` creates the axis label with `axes.label*` rcParams, but `Axis.clear()` (called when an Axes is created/cleared) calls `label._reset_visual_defaults()`, which resets the label to the generic `text.color`/`font.size`/`font.weight` defaults. The `axes.labelsize`, `axes.labelcolor` and `axes.labelweight` rcParams were therefore silently ignored, while values passed explicitly in the script still worked (S3: default styling despite requested custom values).

Change: in `Axis.clear()`, after resetting the label, reapply color, fontsize and fontweight from the `axes.label*` rcParams.

Verification: added `test_axis_label_rcparams` in test_axes.py (fails before, passes after); ran test_axes.py, test_text.py.
