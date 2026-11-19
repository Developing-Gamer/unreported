Fix protected-access / unused-private-member false positives in static methods

## Problem
A `@staticmethod` that builds an instance of its own class and reads or assigns a protected/private attribute on it (`instance.__value = value`) was reported as `protected-access` (W0212), and the private attribute as `unused-private-member` (W0238). The own-instance exemption added for #1159 applied only to classmethods.

## Fix
- `_check_protected_attribute_access` now applies the exemption to static methods too (`_is_classmethod_or_staticmethod`).
- `_check_unused_private_attributes` treats an attribute assigned via a name inferred to be an instance of the class itself as equivalent to `self.attr`.
- Functional tests added in `access_to_protected_members` (own-instance access/assignment OK; other class still flagged). ChangeLog entry added.

## Verification
- `pytest tests/test_functional.py -k access_to_protected_members` fails before the fix, passes after.
- Full functional + checkers suites: only `recursion_error_3152` and two `unittest_imports` wildcard tests fail, and they fail identically on the base commit.
