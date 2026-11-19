Fix empty string from pytest_make_parametrize_id being ignored

## Overview
A `pytest_make_parametrize_id` hook that returned `""` was treated as "no answer", so pytest fell back to its default id (the value, or argname+index). The hook is documented to return `None` when it doesn't know the value, so `""` is a deliberate id. The hook result is now only ignored when it is `None`.

## Evidence
GitHub issue "Empty string ignored for id renaming": a hook returning `""` for most arguments still got the default id, because `_idval` checked `if hook_id:`.

## Details
- `src/_pytest/python.py`: `_idval` uses `if hook_id is not None:`. This matches the `idfn` branch just above it, which already uses `is not None`.
- `testing/python/metafunc.py`: new `test_pytest_make_parametrize_id_empty_string`. A conftest hook returns `""` for `x` and `"y2"` for `y`, and the test expects the id `test_func[y2-]`.
- `changelog/5811.bugfix.rst`: changelog entry. The issue number is a guess, so rename the file to the real issue number.
- Ids made only of empty parts can be duplicates; `idmaker` already adds numeric suffixes for those.

## Verification
- Before the fix: `python -m pytest testing/python/metafunc.py -k empty_string -q` fails. It collects `test_func[y2-1]` instead of `test_func[y2-]`.
- After the fix: the same command passes.
- `python -m pytest testing/python/metafunc.py -q`: 99 passed, 1 xfailed.
