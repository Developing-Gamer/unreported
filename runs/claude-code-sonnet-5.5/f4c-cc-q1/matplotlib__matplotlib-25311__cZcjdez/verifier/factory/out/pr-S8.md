Fix pickling of figures with draggable legends and annotations

## Root cause
`DraggableBase.__init__` stored `figure.canvas` in `self.canvas`. Draggable helpers are referenced from the legend/annotation and so are pickled with the figure. `Figure.__getstate__` drops the canvas, but the helper still held its own reference. With a GUI canvas (e.g. `FigureCanvasQTAgg`) this raised `TypeError: cannot pickle 'FigureCanvasQTAgg' object`.

## Change
In `lib/matplotlib/offsetbox.py`, `DraggableBase.canvas` is now a property that returns `ref_artist.figure.canvas`. The canvas captured at construction is kept in `_canvas` only as a fallback for when the artist has been removed from its figure. `__getstate__` leaves `_canvas` and the blit `background` out of the pickled state.

## Verification
Added `test_pickle_draggable_legend_and_annotation` in `lib/matplotlib/tests/test_pickle.py`. It uses a canvas whose pickling raises and a figure with a draggable legend and draggable annotation. The test fails before the change and passes after it. The pickle, legend, offsetbox and text test modules pass, except `test_pickle_load_from_subprocess`, which fails in this checkout and also failed with my changes stashed. `test_warn_big_data_best_loc` failed once in a combined run but passes in isolation and in the pickle+legend run, so it looks order-dependent.
