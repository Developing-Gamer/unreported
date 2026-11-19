Fix conftest loading on Windows when path casing differs (#5792)

Root cause: `unique_path()` applied `os.path.normcase` to the realpath, which lowercases the whole path on Windows. The lowercased path was then used to import conftest.py, so the module name/package root derived from it no longer matched the real filesystem casing, giving `ModuleNotFoundError: No module named 'python'` (pytest 5.1.2 regression).

Change: removed `unique_path`. `_importconftest` now keys `_conftestpath2mod` with `Path(str(conftestpath)).resolve()` (which yields the true on-disk casing and still dedups symlinks), and `_getconftestmodules` uses `directory.realpath()`. `confcutdir` is no longer normcased. Tests in testing/test_conftest.py updated accordingly.

Verification: testing/test_conftest.py, test_pastebin.py, test_capture.py pass on Linux (166 passed). The Windows-specific casing behaviour could not be exercised on this platform.
