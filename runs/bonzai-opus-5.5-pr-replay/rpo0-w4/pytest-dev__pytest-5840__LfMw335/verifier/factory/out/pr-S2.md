Fix conftest import failing on Windows with upper-case folder names (5.1.2 regression)

## Problem
pytest 5.1.2 (#5792) introduced `unique_path()`, which returns `normcase(realpath(path))`. On Windows that lower-cases the whole path. `_getconftestmodules` and `_importconftest` used that lower-cased path to import the conftest, so the module name was built from lower-cased folders (`python.pisys.conftest`) and the import failed: `ImportError while loading conftest 'c:\azure\kms\componenttest\python\pisys\conftest.py'. ModuleNotFoundError: No module named 'python'`.

## Fix
- `_importconftest` now only uses `Path(str(conftestpath)).resolve()` as the `_conftestpath2mod` cache key (still deduplicates symlinks and resolves to the on-disk case on Windows) and imports from the original path.
- `_getconftestmodules` and `confcutdir` no longer go through `unique_path`.
- `unique_path` is removed (no remaining users).
- Changelog `5806.bugfix.rst`.

## Verification
- New test `testing/test_conftest.py::test_conftest_in_package_with_uppercase_folder` simulates the lower-casing normcase. On the base commit it fails with `ConftestImportFailure ... ENOENT .../python/pisys/conftest.py`; passes after the fix.
- `testing/test_conftest.py`, `test_config.py`, `test_collection.py`, `test_pathlib.py`: all pass except two `test_pytest_plugins_in_non_top_level_conftest_unsupported_pyargs` tests, which fail identically on the base commit.
- Not run on real Windows.
