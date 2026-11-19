Fix rename_parameter discarding a deprecated keyword's value when the new keyword is also passed

## Overview
Older scripts using a deprecated (renamed) keyword got default styling instead of the value they asked for. `_api.rename_parameter` used `kwargs.setdefault(new, kwargs.pop(old))`, so when the new name was also passed explicitly (as pyplot wrappers and `super()` calls do, usually with the default), the old-name value was dropped. Its docstring says the old value must be used.

## Details
- `lib/matplotlib/_api/deprecation.py`: use `kwargs[new] = kwargs.pop(old)` so the old-name value always wins.
- `lib/matplotlib/tests/test_api.py`: new `test_rename_parameter_old_and_new_passed`.

## Proof
Before: `f(new=1, old=5)` returned 1 (`assert 1 == 5`). After: returns 5.

## Verification
`python -m pytest lib/matplotlib/tests/test_api.py lib/matplotlib/tests/test_pyplot.py::test_copy_docstring_and_deprecators` -> 13 passed (new test failed on base).
