Raise ValueError for empty Blueprint names

Root cause: `Blueprint.__init__` only rejected names containing a dot, so an empty name was accepted and caused broken endpoint names and registration (see #4944).

Change: `Blueprint.__init__` now raises `ValueError("'name' may not be empty.")` when `name` is empty. I added a changelog entry.

Verification: added `test_empty_name_not_allowed` in tests/test_blueprints.py and ran `pytest tests/test_blueprints.py`.
