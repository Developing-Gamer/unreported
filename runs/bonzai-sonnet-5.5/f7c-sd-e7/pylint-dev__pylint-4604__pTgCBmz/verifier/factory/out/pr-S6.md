Fix unused-import false positive for a module used in a dotted type comment

## Overview
`import abc` followed by `X = ...  # type: abc.ABC` was reported as `unused-import` (W0611), although the module is used in the type comment. The checker now records the module name of dotted type annotations, so the import counts as used.

## Cause
`VariablesChecker._store_type_annotation_node` only recorded the names of a bare `Name` (`ABC`) or a `Subscript` (`List[int]`). A dotted annotation such as `abc.ABC` is an `Attribute` node, so the function returned without recording `abc`, and `_check_imports` then reported the import as unused.

## Changes
- `pylint/checkers/variables.py`: for an `Attribute` annotation, recurse into its `expr`. This records `abc` for `abc.ABC` and `collections` for `collections.abc.Sized`.
- `tests/functional/u/unused/unused_module_type_comment.py`: new functional test, expecting no messages.
- `ChangeLog` entry.

## Proof
Before: `python -m pytest tests/test_functional.py -k unused_module_type_comment` fails with `Unexpected in testdata: 2: unused-import, 3: unused-import`. After: it passes.

## Verification
`python -m pytest tests/test_functional.py -k unused_module_type_comment` passes. Running `-k "unused or typing or type_comment"` together with `tests/checkers/unittest_variables.py` gives the same 8 other failures before and after the change (unused_import, unused_import_py30, unused_variable and several typing_* tests). They are not caused by this change and appear to come from the installed astroid/Python version.

Not covered: `import a.b` used only as `a.b.C` in a type comment is still reported, because dotted imports are matched by their full name. That is a separate problem from this issue.
