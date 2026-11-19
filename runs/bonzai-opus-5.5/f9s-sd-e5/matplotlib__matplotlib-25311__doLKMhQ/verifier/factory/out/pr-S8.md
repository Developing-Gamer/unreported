Fix pickling of figures with a draggable legend or annotation

Pickling a figure whose legend (or annotation) was made draggable raised `TypeError: cannot pickle 'FigureCanvasQTAgg' object`. `DraggableBase.__init__` stored the canvas as an instance attribute (`self.canvas`), so the helper kept in `Legend._draggable` / `Annotation._draggable` dragged the canvas into the pickle even though `Figure.__getstate__` deliberately drops it.

## Details
- `DraggableBase.canvas` is now a read-only property returning `self.ref_artist.figure.canvas`, so it is never part of the pickled state and after unpickling it resolves to the new figure's canvas.
- `DraggableBase.disconnect()` returns early when the artist no longer has a figure (the canvas is then unreachable; the callbacks are weakly referenced and die with the helper). Previously it used the stored canvas.
- Regression test `test_draggable_pickle` in `lib/matplotlib/tests/test_pickle.py`: a figure with an unpicklable canvas, a draggable legend and a draggable annotation is pickled and unpickled.

## Verification
- New test fails before the fix with `TypeError: cannot pickle 'UnpicklableCanvas' object`, passes after.
- `pytest lib/matplotlib/tests/test_pickle.py test_legend.py test_offsetbox.py test_text.py`: all pass except `test_pickle_load_from_subprocess[png]`, which fails identically on the base commit (version-mismatch UserWarning in this environment).
