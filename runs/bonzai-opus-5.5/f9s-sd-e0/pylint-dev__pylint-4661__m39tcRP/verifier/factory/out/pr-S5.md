Fix missing-raises-doc false positive for exceptions documented with multi-dot names

## Problem
Methods whose docstring documents a fully qualified exception such as `mypkg.errors.ValueError` still got W9006 (`"ValueError" not documented as being raised`).

## Cause
`docparams.visit_raise` reduced documented names with `exc.split(".", 1)[-1]`, which strips only the first component, so `mypkg.errors.ValueError` became `errors.ValueError` and never matched the raised `ValueError`. Single-dot names (`re.error`) worked, so only some methods were affected.

## Fix
Use `exc.split(".")[-1]` to compare the final component (the class name). Added Sphinx, Google and Numpy tests with `mypkg.errors.ValueError` (plain, `~` and `!` prefixes) and a ChangeLog entry.

## Verification
- `python -m pytest tests/extensions/test_check_raise_docs.py`: the 3 new tests fail before the change, all pass after.
- `python -m pytest tests/extensions`: passes.
