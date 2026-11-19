Require a non-empty name for Blueprints

## Overview
A `Blueprint` created with an empty name (or registered with `name=""`) was accepted, but then registered un-prefixed endpoints (the leading dot is stripped). `Request.blueprint` returns None for those endpoints, so the blueprint's `before_request` hooks, error handlers and context processors were silently skipped. Flask now raises `ValueError("'name' may not be empty.")` in both places. Issue: "Require a non-empty name for Blueprints" (related to #4944).

## Details
- `Blueprint.__init__` raises `ValueError` when `name` is empty.
- `Blueprint.register` raises `ValueError` when the effective name (`options["name"]` or `self.name`) is empty.
- Added `test_empty_name_not_allowed` in `tests/test_blueprints.py`; before the fix it fails with `DID NOT RAISE <class 'ValueError'>`.
- CHANGES.rst entry under 2.3.0.

## Verification
- `PYTHONPATH=src python -m pytest tests/test_blueprints.py -k empty_name -q`: fails before, passes after.
- Full `pytest tests`: 463 passed; 3 failures in tests/test_cli.py (`CliRunner.__init__() got an unexpected keyword argument 'mix_stderr'`, installed click version) are unrelated to this change.
