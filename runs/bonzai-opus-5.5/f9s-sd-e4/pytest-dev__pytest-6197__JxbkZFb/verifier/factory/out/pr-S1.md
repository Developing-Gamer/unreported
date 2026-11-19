Fix regression: don't import non-test package __init__.py during collection (#6194)

## Overview
pytest 5.2.3 imports every package's `__init__.py` during collection, even when it matches no `python_files` pattern and holds no tests. A package that cannot be imported on the current platform (for example a Windows-only one) now fails the run with a collection error. This restores the 5.2.2 behaviour.

## Cause
`Package.collect` in `src/_pytest/python.py` called `self._mount_obj_if_needed()`, added in 5.2.3 for #5830. That imports `__init__.py` as soon as the package is collected, so `assert False` in `foobar/__init__.py` raised a collection error.

## Change
- Remove the eager `_mount_obj_if_needed()` call from `Package.collect`. `Package.setup` still imports the package when tests under it run, and `__init__.py` is still collected as a module when it matches `python_files`.
- Add `test_does_not_collect_non_test_package_init`: a package whose `__init__.py` is `assert False`, plus a passing `test_a.py`. It must report `1 passed`.
- Remove `test_skip_package`. It asserted the #5830 behaviour (`pytestmark` in `__init__.py` skipping the tests next to it), which required the eager import. #5830 needs a narrower fix that doesn't import non-test packages.
- Add a changelog entry.

## Verification
- Before the fix the new test fails with `ERROR collecting foobar/__init__.py ... assert False` and `1 errors during collection`. After the fix it passes.
- `testing/test_collection.py`, `testing/test_skipping.py`, `testing/test_session.py` and `testing/python` (without `metafunc.py`, which needs `hypothesis`): the only new failure against the base was `test_skip_package`, now removed. The other failures also fail on the base commit.
