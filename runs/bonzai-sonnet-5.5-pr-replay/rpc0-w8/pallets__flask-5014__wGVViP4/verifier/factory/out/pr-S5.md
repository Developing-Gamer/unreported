Raise ValueError when a Blueprint is given an empty name

## Overview
`Blueprint("", __name__)` was accepted silently, creating a blueprint with an empty registered name; routing and endpoint handling then misbehave (see #4944) with no clear error. `Blueprint.__init__` now raises `ValueError("'name' may not be empty.")`, next to the existing dot check.

## Proof
- Before: `pytest tests/test_blueprints.py -k empty_name` fails with `Failed: DID NOT RAISE <class 'ValueError'>`.
- After: the same command passes; `tests/test_blueprints.py` is 60 passed.

## Details
- `src/flask/blueprints.py`: add the empty-name check.
- `tests/test_blueprints.py`: add `test_empty_name_not_allowed`.
- `CHANGES.rst`: changelog entry.

## Verification
Full `pytest tests` has 11 failures (DeprecationWarning in test_testing.py etc.), identical on the base commit, caused by the environment's newer dependency versions and unrelated to this change.
