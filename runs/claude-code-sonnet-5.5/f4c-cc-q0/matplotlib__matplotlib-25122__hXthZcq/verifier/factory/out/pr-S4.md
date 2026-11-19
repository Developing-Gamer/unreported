Prefer already-imported PySide6 over PyQt5 in qt_compat

Root cause: when a Qt binding was already imported, `qt_compat` checked `PyQt6`, `PyQt5`, `PySide6`, `PySide2` in that order. With both PySide6 and PyQt5 loaded, PyQt5 (Qt 5) won, contrary to the intended Qt6-first ordering.

Change: check `PyQt6`, `PySide6`, `PyQt5`, `PySide2` in that order.

Verification: added `test_qt_api_prefers_qt6_family_when_already_imported` in test_backend_qt.py (real PyQt5 plus a faked PySide6; fails before the change, passes after). PySide6 is not installed here, so the test uses a stub.
