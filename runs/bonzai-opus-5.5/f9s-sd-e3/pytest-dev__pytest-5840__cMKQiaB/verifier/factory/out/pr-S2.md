Fix conftest import with lowercased paths on Windows (5.1.2 regression)

## Overview
pytest 5.1.2 (#5792) added `unique_path()`, which returns `normcase(realpath)`. On Windows this lowercases the whole path. `_getconftestmodules` and `_importconftest` then used that path to import the conftest, so the module name was built from lowercased folder names (`python.pisys.conftest`) and the import failed with `ModuleNotFoundError: No module named 'python'` when the folder is `Python`.

## Details
- `_importconftest` now uses `Path(str(conftestpath)).resolve()` only as the `_conftestpath2mod` cache key (resolve() returns the on-disk casing on Windows, which keeps the #5792 fix) and imports from the original `conftestpath`.
- `_getconftestmodules` walks `directory.realpath().parts()` instead of a lowercased path. `_set_initial_conftests` no longer lowercases `confcutdir`.
- `unique_path` is removed (no longer used).
- Test: `test_conftest_import_preserves_folder_case` (simulates a lowercasing normcase so it fails on Linux too on the base commit: the conftest in `Python/PIsys` is never loaded, `fixture 'myfix' not found`). The existing `test_conftest_badcase` (#5792) covers Windows.
- Changelog: `changelog/5819.bugfix.rst`.

## Verification
`python -m pytest testing/test_conftest.py testing/test_pathlib.py testing/test_config.py testing/test_collection.py` (py3.9): all pass except 2 `test_pytest_plugins_in_non_top_level_conftest_unsupported_pyargs` failures (pkg_resources DeprecationWarning), which fail identically on the base commit. Not run on Windows.
