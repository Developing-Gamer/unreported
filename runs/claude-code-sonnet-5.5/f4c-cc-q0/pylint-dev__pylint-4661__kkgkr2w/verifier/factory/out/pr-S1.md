Fix protected-access false positive for instance access in static methods

Root cause: `ClassChecker._check_protected_attribute_access` exempted accesses on an inferred instance of the enclosing class (to an attribute that exists on the class) only inside classmethods. A `@staticmethod` of the same class creating an instance and setting `instance.__value` was therefore reported as `protected-access`.

Change: replaced `_is_classmethod` with `_is_classmethod_or_staticmethod` (pylint/checkers/classes.py), so the same exemption applies to static methods. Accesses on instances of other classes are still reported.

Verification: added `Issue3178` cases to tests/functional/a/access/access_to_protected_members.py/.txt (no message for same-class instance, message kept for another class); the test fails without the fix. Full test suite passes except `recursion_error_3152`, which also fails on the untouched checkout.
