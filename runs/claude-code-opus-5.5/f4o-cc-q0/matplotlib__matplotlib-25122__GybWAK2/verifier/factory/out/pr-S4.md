Fix Qt binding priority when both PySide6 and PyQt5 are already imported

## Root cause
`lib/matplotlib/backends/qt_compat.py` first looks for a Qt binding that is already imported. Its module docstring says it checks PyQt6, PySide6, PyQt5, PySide2, in that order. The code actually checked `PyQt5.QtCore` before `PySide6.QtCore`. So in a process where both PySide6 and PyQt5 were loaded, Matplotlib chose PyQt5 and embedded plots used Qt 5 widgets instead of the Qt 6 interface they used before.

## Change
- Swap the two `sys.modules` checks so the order matches the docs: PyQt6, PySide6, PyQt5, PySide2.
- Add `lib/matplotlib/tests/test_qt_compat.py`. It puts fake binding modules into `sys.modules` in a subprocess, imports `qt_compat`, and checks which `QT_API` is selected for several combinations of already-imported bindings. It needs no real Qt install, so it runs on CI machines without Qt.

## Verification
- `pytest lib/matplotlib/tests/test_qt_compat.py`: 4 passed.
- Without the fix, the two cases that load both PyQt5 and PySide6 fail (PyQt5 is selected).
