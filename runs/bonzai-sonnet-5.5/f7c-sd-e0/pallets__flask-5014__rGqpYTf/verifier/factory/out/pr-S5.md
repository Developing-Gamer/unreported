Require a non-empty name for Blueprints

## Overview
`Blueprint("", __name__)` was accepted, producing a blueprint with an empty name that misbehaves in routing and endpoint handling (#4944). `Blueprint.__init__` now raises `ValueError("'name' may not be empty.")`, alongside the existing dot check.

## Proof
- Before: `pytest tests/test_blueprints.py -k empty_name` fails with `Failed: DID NOT RAISE <class 'ValueError'>`.
- After: the same command passes.

## Details
- `src/flask/blueprints.py`: empty-name check in `Blueprint.__init__`.
- `tests/test_blueprints.py`: `test_empty_name_not_allowed`.
- `CHANGES.rst`: changelog entry.

## Verification
`pytest tests/test_blueprints.py` passes. The full suite has 11 failures from werkzeug DeprecationWarnings in the environment, unrelated to this change (checked against base).
