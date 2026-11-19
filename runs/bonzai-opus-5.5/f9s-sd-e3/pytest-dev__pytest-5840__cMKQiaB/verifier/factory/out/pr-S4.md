Accept an empty string from pytest_make_parametrize_id as a valid test id

## Overview
`_idval` checked the result of the `pytest_make_parametrize_id` hook with `if hook_id:`, so a hook that returned `""` was treated as "no answer" and pytest fell back to its default id. The hook contract says only `None` means the hook does not know the value (and the `ids=` callable path already keeps `""`). The check is now `if hook_id is not None:`, so `""` is used as the id.

## Evidence
GitHub issue: "Empty string ignored for id renaming" — a hook returning `""` for most arguments still gets the default id.

## Details
- `src/_pytest/python.py`: `if hook_id:` -> `if hook_id is not None:` in `_idval`.
- `testing/python/metafunc.py`: `test_pytest_make_parametrize_id_empty_string` — conftest hook returns `""` for `x` and `None` otherwise; `--collect-only -q` must list `test_func[-2]` and `test_func[-4]`.
- `changelog/5806.bugfix.rst` (issue number is a guess; rename to the real issue number).

## Verification
Python 3.9 (testbed env), `python -m pytest testing/python/metafunc.py -q -k make_parametrize_id`:
- before the fix: new test fails (collected `test_func[1-2]`, `test_func[3-4]`)
- after the fix: `99 passed, 1 xfailed` for all of `testing/python/metafunc.py`.
