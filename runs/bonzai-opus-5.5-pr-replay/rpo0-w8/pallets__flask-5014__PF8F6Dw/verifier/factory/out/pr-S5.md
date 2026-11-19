Require a non-empty name for Blueprints

## Overview
A `Blueprint` created with an empty name was accepted. Its endpoints then lost their blueprint prefix (`f"{prefix}.{name}.{endpoint}".lstrip(".")`), so `request.blueprint` was `None` and the blueprint's `before_request` hooks, error handlers and context processors were silently never applied (see #4944). Creating or registering a blueprint with an empty name now raises `ValueError("'name' may not be empty.")`.

## Details
- `Blueprint.__init__` rejects an empty name, next to the existing dot check.
- `Blueprint.register` rejects an empty `name=` option, which had the same effect.
- Tests added in `tests/test_blueprints.py` for both paths; they failed with "DID NOT RAISE" before the change.
- CHANGES.rst entry added.

## Verification
- `python -m pytest tests/test_blueprints.py -k empty_name`: 2 failed before, 2 passed after.
- `python -m pytest tests/test_blueprints.py`: 61 passed.
- Full `tests`: the same 8 failures (DeprecationWarning in test_testing.py) before and after; unrelated.
