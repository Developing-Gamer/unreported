Fix missing-raises-doc false positive for exceptions documented with multi-dot names

## Overview
The docparams checker reduced documented exception names to their class name with `split(".", 1)[-1]`, which removes only the first dot. A docstring entry such as `:raises package.errors.ValueError:` became `errors.ValueError`, never matched the raised `ValueError`, and `missing-raises-doc` (W9006) was reported even though the exception was documented. It now uses `rsplit(".", 1)[-1]`, keeping only the last component.

## Details
- `pylint/extensions/docparams.py`: `visit_raise` uses `rsplit` to extract the class name.
- Tests added in `tests/extensions/test_check_docs.py` for Sphinx and Google docstrings with `package.errors.ValueError`; both failed before the change (W9006 emitted for `ValueError`) and pass now.
- ChangeLog entry added.

## Verification
`python -m pytest tests/extensions/test_check_docs.py -q` -> 124 passed.
