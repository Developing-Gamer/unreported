Fix 5.2.3 regression: stop importing non-test `__init__.py` files during collection

## Overview
Since 5.2.3, pytest imports every `__init__.py` found under the collected directories, even when it does not match `python_files`. A package that cannot be imported on the current platform (or simply contains `assert False`) now breaks the whole run with a collection error. After this change such files are no longer imported unless they match `python_files`, as in 5.2.2.

## Details
- Cause: the #5830 fix added `self._mount_obj_if_needed()` at the start of `Package.collect()`. That imports the package's `__init__.py` before checking whether it matches `python_files`.
- Fix: remove that call. `__init__.py` files matching `python_files` are still imported through the existing `Module(init_module, self)` branch, and `Package.setup()` still imports lazily when it needs `setup_module`.
- Trade-off: this reverts the #5830 behaviour (a `pytestmark = skip` in a non-test `__init__.py` applied to the package's tests). That cannot be kept without importing the file at collection, which is the bug. The `test_skip_package` test for it is removed.
- Added regression test `test_collect_does_not_import_non_test_init_files` in `testing/test_collection.py`; changelog `changelog/6194.bugfix.rst`.

## Verification
- New test fails on the base commit (`collected 1 item / 1 errors`, `ERROR collecting foobar/__init__.py`, `AssertionError`) and passes after the fix.
- Ran `testing/test_collection.py testing/python/collect.py testing/test_skipping.py testing/python/fixtures.py testing/acceptance_test.py` before and after. The same 16 tests fail in both runs (environment-related, e.g. DeprecationWarning, setuptools entry points). There are no new failures.
