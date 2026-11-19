Fix Qt binding selection order when PySide6 and PyQt5 are both already imported

## Overview
In sessions where both PySide6 and PyQt5 were already loaded, embedded Matplotlib plots were built from Qt 5 widgets (PyQt5) instead of Qt 6 ones, although the host used PySide6. The "already imported" check in `qt_compat.py` tested PyQt5 before PySide6, contradicting the documented order (PyQt6, PySide6, PyQt5, PySide2) and the fallback candidate list.

## Details
- `lib/matplotlib/backends/qt_compat.py`: check `PySide6.QtCore` before `PyQt5.QtCore`.
- `lib/matplotlib/tests/test_backend_qt.py`: new `test_already_imported_binding_order` runs a subprocess with stub PySide6 and PyQt5 modules in `sys.modules` and asserts `QT_API == "PySide6"`. Before the fix it yielded `PyQt5`.

## Verification
`pytest lib/matplotlib/tests/test_backend_qt.py -k binding_order` fails before (`'PyQt5' == 'PySide6'`) and passes after; the rest of test_backend_qt.py was run too.
