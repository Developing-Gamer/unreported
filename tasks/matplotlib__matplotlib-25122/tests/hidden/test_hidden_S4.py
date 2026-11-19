import os
import subprocess
import sys
import textwrap


def test_preimported_pyside6_takes_precedence_over_pyqt5():
    script = textwrap.dedent('''
        import os
        import sys
        import types

        import matplotlib

        os.environ.pop("QT_API", None)

        def add_binding(name, version):
            package = types.ModuleType(name)
            package.__path__ = []
            package.__version__ = ".".join(map(str, version))

            core = types.ModuleType(name + ".QtCore")
            core.__package__ = name
            core.PYQT_VERSION_STR = package.__version__
            core.pyqtSignal = object()
            core.pyqtSlot = object()
            core.pyqtProperty = object()
            core.QLibraryInfo = types.SimpleNamespace(
                version=lambda: types.SimpleNamespace(
                    segments=lambda: version,
                    toString=lambda: package.__version__,
                )
            )
            gui = types.ModuleType(name + ".QtGui")
            widgets = types.ModuleType(name + ".QtWidgets")
            widgets.QFileDialog = types.SimpleNamespace(
                getSaveFileName=lambda *args, **kwargs: ("", "")
            )
            package.QtCore = core
            package.QtGui = gui
            package.QtWidgets = widgets
            sys.modules[name] = package
            for module in (core, gui, widgets):
                sys.modules[module.__name__] = module

        # Model an embedding application with both bindings already imported,
        # without requiring native Qt libraries or a display server.
        add_binding("PySide6", (6, 4, 0))
        add_binding("PyQt5", (5, 15, 2))
        shiboken = types.ModuleType("shiboken6")
        shiboken.isValid = lambda obj: True
        sys.modules["shiboken6"] = shiboken
        sip = types.ModuleType("sip")
        sip.isdeleted = lambda obj: False
        sys.modules["sip"] = sip

        from matplotlib.backends import qt_compat

        assert qt_compat.QT_API == "PySide6", qt_compat.QT_API
        assert qt_compat.QtCore is sys.modules["PySide6.QtCore"]
    ''')
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(sys.path)
    result = subprocess.run(
        [sys.executable, "-c", script],
        env=env,
        capture_output=True,
        text=True,
        timeout=8,
    )
    assert result.returncode == 0, result.stdout + result.stderr
