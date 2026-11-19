Fix 5.2.3 regression: don't import non-test package __init__.py during collection (#6194)

## Overview
pytest 5.2.3 imported every package's `__init__.py` during collection, even when it matches no `python_files` pattern. A non-test package that cannot be imported on the current platform (e.g. `assert False` or a Windows-only import) now fails the whole run with a collection error.

## Cause
The #5830 change added `self._mount_obj_if_needed()` at the start of `Package.collect`. That imports the package's `__init__.py` for every package, whether or not it holds tests.

## Fix
Remove that call, restoring 5.2.2 behaviour. `test_skip_package` (which tested the #5830 behaviour) is removed, so #5830 is effectively reopened and needs a narrower fix. A changelog entry is added.

## Proof
- New test `testing/test_collection.py::test_does_not_collect_non_test_package_init`: `foobar/__init__.py` containing `assert False` plus a passing `test_a.py`.
  - Before: `collected 1 item / 1 errors`, `ERROR collecting foobar/__init__.py`.
  - After: `1 passed`.

## Verification
`python -m pytest testing/test_collection.py testing/python/collect.py testing/test_skipping.py testing/test_session.py testing/test_assertrewrite.py testing/test_mark.py testing/test_doctest.py`. The failing set is identical to the base commit (pre-existing failures from Python 3.9 / newer deps).
