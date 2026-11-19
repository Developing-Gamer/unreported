Fix ImportError loading conftest on Windows due to lowercased path (#5792)

## Evidence
pytest 5.1.2 on Windows: `ImportError while loading conftest 'c:\azure\kms\componenttest\python\pisys\conftest.py'. ModuleNotFoundError: No module named 'python'` (5.1.1 worked).

## Cause
`_importconftest` and `_getconftestmodules` replaced the conftest path/directory with `unique_path(...)` (realpath + normcase, lowercase on Windows) and then imported / walked that path. The package root and module name were derived from the lowercased path and no longer matched the real directory names.

## Fix
- `_importconftest`: `unique_path()` is used only as the key in `_conftestpath2mod` / `_dirpath2confmods`; the module is imported from the case-preserving `realpath()`.
- `_getconftestmodules`: walks the case-preserving real directory, uses the normalized path only as cache key; the confcutdir comparison normalizes the parent.
- Test `test_conftest_import_preserves_path_case` (patches `normcase` to lowercase, so it reproduces on Linux); existing tests now compare `__file__` against the real path.

## Verification
`pytest testing/test_conftest.py testing/test_config.py testing/test_collection.py testing/acceptance_test.py`: the same 11 pre-existing failures (environment, e.g. DeprecationWarnings) before and after; new test passes. Not run on real Windows.
