Fix unused-import false positive for modules used in attribute type comments

Root cause: `_store_type_annotation_node` in `pylint/checkers/variables.py` handled only `Name` and `Subscript` nodes. A type comment such as `# type: abc.ABC` parses to an `Attribute`, so `abc` was never recorded as used and `import abc` was reported as unused.

Change: for an `Attribute` annotation, recurse into its `expr`, so `abc` is recorded. Added a ChangeLog entry.

Verification: added functional test `tests/functional/u/unused/unused_import_type_comment_attribute.py`, built from the issue's reproducer. The unused-import functional tests and `tests/checkers/unittest_variables.py` pass.
