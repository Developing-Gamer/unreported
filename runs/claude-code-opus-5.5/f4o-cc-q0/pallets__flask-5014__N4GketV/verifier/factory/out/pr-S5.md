Raise ValueError when a Blueprint is given an empty name

## Root cause
`Blueprint.__init__` only checked that `name` had no `.` in it. An empty
string was accepted, and it breaks things later: endpoint prefixes become
`.endpoint`, the app registers the blueprint under `""`, and nested names
come out wrong (see #4944).

## Change
- `src/flask/blueprints.py`: raise `ValueError("'name' may not be empty.")`
  in `Blueprint.__init__` when `name` is empty, before the existing dot check.
- `tests/test_blueprints.py`: add `test_empty_name_not_allowed`.
- `CHANGES.rst`: add a changelog entry.

## Verification
- `pytest tests/test_blueprints.py`: 60 passed, including the new test.
- Full suite: 8 failures, the same 8 as on the unmodified checkout
  (DeprecationWarning-related tests in the environment); no new failures.
