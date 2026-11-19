Fix pytest importing unrelated `__init__.py` files during collection (regression in 5.2.3)

## Overview
pytest 5.2.3 imported the `__init__.py` of every package directory it visited, even when the package contained no tests and `__init__.py` did not match `python_files`. A package such as `foobar/__init__.py` containing `assert False` (or a Windows-only package) broke the whole run with a collection error. Such packages are no longer imported unless there are tests to run inside them.

## Cause
The #5830 fix put `self._mount_obj_if_needed()` at the top of `Package.collect()`. That imports `__init__.py` as soon as the package node is collected, before anything checks whether it is relevant.

## Fix
- Removed the unconditional import from `Package.collect()`.
- `Module.collect()` now mounts the enclosing `Package` nodes, so a `pytestmark` in a package's `__init__.py` is still known before test setup (keeps #5830 / `test_skip_package` working). A package is therefore imported only when a test module inside it is collected, as it was before 5.2.3.

## Proof
- Before: `testing/test_collection.py::test_does_not_import_unrelated_init_py` fails with `ERROR collecting foobar/__init__.py ... assert False`, `collected 1 item / 1 errors`.
- After: it passes (1 passed); `testing/test_skipping.py::test_skip_package` still passes.

## Verification
Ran test_collection, python/collect, test_skipping, test_pluginmanager, test_conftest, test_doctest, test_terminal, test_session and python/fixtures. 20 tests fail identically with and without the change (environment-related, e.g. plugin and header tests); no new failures.
