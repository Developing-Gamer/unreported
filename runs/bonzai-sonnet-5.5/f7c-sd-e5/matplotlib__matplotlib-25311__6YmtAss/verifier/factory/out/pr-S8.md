Fix pickling of figures with a draggable legend or annotation

`DraggableBase.__init__` stored `figure.canvas` as an instance attribute. `Figure.__getstate__` drops the canvas, but the draggable helper (held by `Legend._draggable` / `Annotation._draggable`) still referenced it, so `pickle.dumps(fig)` failed with e.g. `TypeError: cannot pickle 'FigureCanvasQTAgg' object`.

`canvas` is now a property reading `ref_artist.figure.canvas`, so the helper holds no canvas reference and the figure pickles.

Test: `test_pickle.py::test_draggable_legend_and_annotation` gives the canvas an unpicklable attribute (like a GUI canvas) and round-trips a figure with a draggable legend and annotation. Before: `TypeError: cannot pickle '_thread.lock' object`; after: passes. test_legend.py and test_offsetbox.py pass; test_pickle_load_from_subprocess fails only due to a version-mismatch warning unrelated to this change.
