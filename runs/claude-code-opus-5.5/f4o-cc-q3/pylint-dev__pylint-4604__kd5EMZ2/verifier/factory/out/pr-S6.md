Fix unused-import false positive for modules used via attribute access in type comments

## Root cause
`VariablesChecker._store_type_annotation_node` (pylint/checkers/variables.py) records the names
used by type annotations and type comments, so that imports used only there are not reported
as `unused-import`. It handled `Name` nodes (`# type: ABC`) and `Subscript` nodes
(`# type: List[int]`). For any other node it returned early. An attribute annotation such as
`# type: abc.ABC` is an `Attribute` node, so `abc` was never recorded and `import abc` was
reported as unused.

## Change
When the annotation is an `astroid.Attribute`, recurse into its `.expr`. Dotted chains like
`a.b.c` therefore resolve to the base name `a`.

## Verification
- Added cases to `tests/functional/u/unused/unused_import.py`: `import abc` / `from abc import ABC`,
  used only in `# type: abc.ABC` and `# type: ABC` comments.
- Without the fix the functional test fails with an unexpected `unused-import` on line 66. With the
  fix it passes.
- `tests/test_functional.py` and `tests/checkers/unittest_variables.py`: 515 passed, 1 failed. The one
  failure, `recursion_error_3152`, also fails on the unmodified checkout and is unrelated.
