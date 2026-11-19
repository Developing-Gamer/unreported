Fix false positive protected-access in static methods

## Root cause
`ClassChecker._check_protected_attribute_access` (pylint/checkers/classes.py) accepts `instance._attr` outside `self`/`cls` when the enclosing function is a classmethod, the expression is inferred to be an instance of the enclosing class, and the attribute exists on that class. Static methods were not covered, so code like the following was reported as `protected-access`:

```python
class Clazz:
    @staticmethod
    def create(value):
        instance = Clazz()
        instance.__value = value
```

## Change
- Added `_is_classmethod_or_staticmethod` and used it in place of `_is_classmethod` for that exemption. Inside a static method, accessing a protected member of an instance of the same class is now allowed. Access on instances of other classes is still reported.
- Documented the case in the method docstring and added a ChangeLog entry.

## Verification
- Added `Issue2914` to `tests/functional/a/access/access_to_protected_members.py`/`.txt`: no message inside the static method for its own class, and a message is still expected when a static method accesses another class's protected member. This test fails without the fix and passes with it.
- Ran the reproducer from the issue with only `protected-access` enabled: no message.
- `pytest tests/test_functional.py tests/checkers tests/lint tests/extensions tests/testutils`: everything passes except `recursion_error_3152`, which also fails on the unmodified checkout (the installed astroid is 2.6.6, but the tests pin 2.6.5).

## Note / follow-up
The issue's snippet also triggers `unused-private-member` (a check added after the reported pylint version) on `instance.__value = value`, because `_check_unused_private_attributes` only counts `self.`/`cls.` reads. That is a separate check and a separate root cause, and it is not changed here. The new functional test disables it inline on that line.
