qt_compat: prefer PySide6 over PyQt5 when both are already imported

## Overview
In sessions where both PySide6 and PyQt5 were already imported, embedded plots started using Qt 5 widgets (PyQt5) instead of the Qt 6 interface. The "already imported" check in `qt_compat.py` tested `PyQt5.QtCore` before `PySide6.QtCore`, contradicting the documented order (PyQt6, PySide6, PyQt5, PySide2) and the order used by the fallback candidate list. The checks are now in the documented order.

## Details
- `lib/matplotlib/backends/qt_compat.py`: swap the `PyQt5.QtCore` and `PySide6.QtCore` branches of the already-imported check.
- `lib/matplotlib/tests/test_backends_interactive.py`: new `test_qt_compat_already_imported_order`, which runs in a subprocess with fake binding modules in `sys.modules` (so it does not need Qt installed) and asserts the chosen `QT_API` for: PyQt5+PySide6 -> PySide6; PySide2+PyQt5+PySide6 -> PySide6; PySide2+PyQt5 -> PyQt5; PySide2+PySide6+PyQt6 -> PyQt6.

## Verification
- Before the fix, the two PySide6 cases fail with `assert 'PyQt5' == 'PySide6'`; after, all 4 pass.
- `test_backends_interactive.py` / `test_backend_qt.py`: the rest pass or are skipped (no Qt/display here). `test_lazy_auto_backend_selection` fails identically on the base commit (its subprocess cannot import matplotlib in this environment), unrelated to this change.
