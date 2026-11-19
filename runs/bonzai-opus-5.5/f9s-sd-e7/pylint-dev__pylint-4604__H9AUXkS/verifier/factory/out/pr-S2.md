Fix unused-import false positive for modules used in attribute lookups in type comments

## Overview
`import foo` followed by `a = ...  # type: foo.Bar` was reported as `unused-import`, because `VariablesChecker._store_type_annotation_node` ignored `astroid.Attribute` annotations. The regression test for #4603 also imports `IS_PYPY` from `pylint.constants`, which did not exist, so `tests/checkers/unittest_variables.py` failed at collection with `ImportError: cannot import name 'IS_PYPY'`.

## Details
- `pylint/checkers/variables.py`: for an `Attribute` annotation, record the names in its `expr` (recursively), so `foo.Bar` marks `foo` as used.
- `pylint/constants.py`: add `IS_PYPY = platform.python_implementation() == "PyPy"`.
- `tests/checkers/unittest_variables.py`: add `test_attribute_in_type_comment` (skipped on PyPy).
- `ChangeLog`: entry, Closes #4603.

## Verification
- `python -m pytest tests/checkers/unittest_variables.py -p no:cacheprovider`: before, collection ImportError on `IS_PYPY`; with only the constant added, the new test fails (unused-import); after the fix, 21 passed.
- `python -m pytest tests/test_functional.py -k 'unused or type_annotation or typing'`: 28 passed, 1 skipped.
