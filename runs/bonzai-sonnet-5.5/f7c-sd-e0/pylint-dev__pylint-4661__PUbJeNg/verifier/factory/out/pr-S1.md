Fix protected-access false positive in static methods

## Overview
`protected-access` was emitted for a static method that builds an instance of its own class and sets/reads a private attribute on it (`instance = Clazz(); instance.__value = value`). The existing exemption for "own instance, attribute defined on the class" only applied to classmethods. It now also applies to staticmethods, which are equally inside the class body.

## Evidence
GitHub issue "False positive protected-access in static method" (snippet with `Clazz.create` as `@staticmethod`).

## Details
- `pylint/checkers/classes.py`: replaced `_is_classmethod` (only used here) with `_is_classmethod_or_staticmethod`; the `_is_inferred_instance` and `_is_class_attribute` guards are kept, so other classes' instances and undefined attributes still warn.
- Tests: extended `tests/functional/a/access/access_to_protected_members.py/.txt` with a staticmethod setting/reading on its own class (no message) and on another class (still `protected-access`).
- ChangeLog entry added.
- Note: the same snippet also triggers `unused-private-member` (separate checker heuristic that only counts `self.` reads); the test disables it on that line and it is not changed here.

## Verification
- `python -m pytest tests/test_functional.py -k access_to_protected`: fails before the fix (unexpected protected-access at the staticmethod lines), passes after.
- `tests/test_functional.py tests/checkers`: only pre-existing failures remain (`recursion_error_3152`, `unittest_imports` wildcard tests), unrelated.
