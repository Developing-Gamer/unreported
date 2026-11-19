Fix conftest ImportError on Windows caused by lowercased paths (#5792)

## Overview
Since 5.1.2, `pytest --collect-only .\PIsys` on Windows failed with `ImportError while loading conftest 'c:\azure\kms\componenttest\python\pisys\conftest.py'. ModuleNotFoundError: No module named 'python'`. The conftest path was passed through `unique_path()` (realpath + `normcase`), which lowercases the whole path on Windows. The lowercased path was then used for `pyimport()`, so the package root/module name no longer matched the real directory names.

## Details
- `_importconftest` now uses `Path(str(conftestpath)).resolve()` only as the key of `_conftestpath2mod` (it yields the right casing on case-insensitive filesystems and still dedupes symlinks), and imports the original conftest path.
- `_getconftestmodules` walks `directory.realpath()` (symlinks resolved, case preserved); `confcutdir` uses `realpath()` likewise.
- `unique_path` is removed from `_pytest.pathlib` (no remaining users).
- Tests: new `test_conftest_import_preserves_case` simulates a lowercasing `normcase` and a mixed-case package dir (runs on Linux; before the fix the conftest is not found at all); existing tests updated to not use `unique_path`. Changelog `5792.bugfix.rst` added.

## Verification
`python -m pytest testing/test_conftest.py testing/test_config.py testing/test_collection.py testing/test_pathlib.py` -> only 2 failures, `test_pytest_plugins_in_non_top_level_conftest_unsupported_pyargs[True/False]`, which also fail on the base commit. The new test fails before the fix and passes after. Not run on real Windows.
