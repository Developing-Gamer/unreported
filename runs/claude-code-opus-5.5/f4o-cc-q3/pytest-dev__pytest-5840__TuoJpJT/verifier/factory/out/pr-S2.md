Fix ImportError loading conftest.py on Windows when directory names contain uppercase letters

## Root cause
pytest 5.1.2 added `_pytest.pathlib.unique_path()`, which runs `os.path.normcase(path.realpath())`. On Windows `normcase` lowercases the path. `PytestPluginManager` then used that lowercased path for the conftest lookup and also for the import itself. `conftestpath.pyimport()` builds the dotted module name from the directory names, so `C:\...\Python\PIsys\conftest.py` was imported as `python.pisys.conftest`, which fails with `ModuleNotFoundError: No module named 'python'`.

## Change
- `src/_pytest/config/__init__.py`: conftest paths are no longer rewritten. Only the cache key in `_importconftest` is normalized, using `Path(str(conftestpath)).resolve()`. This still resolves symlinks and gives the real on-disk casing on case-insensitive filesystems, so a conftest is still loaded only once. The import uses the original path. `--confcutdir` and `_getconftestmodules` no longer use `unique_path`.
- `src/_pytest/pathlib.py`: removed `unique_path`, which is now unused.

## Verification
- `testing/test_conftest.py`: updated the tests that used `unique_path`, and added `test_conftest_uppercase` (a conftest inside an uppercase package directory).
- Ran `testing/test_conftest.py`, `test_pathlib.py`, `test_config.py`, `test_pluginmanager.py`, `acceptance_test.py` and others. There are no new failures. The 19 failures that remain fail the same way on the unmodified tree (environment-related setuptools/entry-point tests).
- Note: verified on Linux only. The Windows lowercasing case itself was not reproduced; `test_conftest_badcase` runs only on case-insensitive filesystems.
