Fix unused-import false positive for modules used in attribute lookups in type comments

## Overview
`tests/checkers/unittest_variables.py` could not be collected: it failed with `ImportError: cannot import name 'IS_PYPY' from 'pylint.constants'` (Sentry ev_s2, 662 events / 114 users in 7 days). The import points at a missing constant and at a missing behaviour: `VariablesChecker` ignored attribute lookups in type comments, so `import foo` followed by `# type: foo.Bar` was reported as `unused-import`. Closes #4603.

## Details
- `pylint/constants.py`: add `IS_PYPY = platform.python_implementation() == "PyPy"`.
- `pylint/checkers/variables.py`: `_store_type_annotation_node` now recurses into `Attribute.expr`, so the base name (`foo` in `foo.Bar`) is recorded as used.
- `tests/checkers/unittest_variables.py`: add `test_attribute_in_type_comment`, skipped on PyPy via `IS_PYPY`.
- `ChangeLog`: entry for #4603.

## Verification
- Before (base commit): `pytest tests/checkers/unittest_variables.py` errors at collection with the `IS_PYPY` ImportError. With only the constant added, the new test fails with an `unused-import` message.
- After: `pytest tests/checkers/unittest_variables.py tests/test_functional.py -k "not functional or unused or type_annotation or typing"` gives 49 passed, 1 skipped.
