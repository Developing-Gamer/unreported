Raise ValueError for an unknown sesame_database instead of silently using "all"

## Overview
`sesame_database.validate` replaced any value other than exactly `all`, `simbad`, `ned` or `vizier` with `all`. A config such as `SIMBAD`, `Ned` or `"simbad "` therefore queried all databases and took the first match, so ambiguous names could resolve to a different position with no error or warning. Invalid values now raise `ValueError("Unknown database '...'")`.

## Evidence
Support report: since a configuration update, a few ambiguous target names return different sky positions, yet every lookup is marked successful with no warnings.

## Proof
Before: `pytest astropy/coordinates/tests/test_name_resolve.py -k sesame_database` -> 5 failed (DID NOT RAISE), 4 passed.
After: all 9 pass.

## Details
- `astropy/coordinates/name_resolve.py`: raise instead of returning "all"; docstring updated.
- Tests for valid and invalid names; changelog `docs/changes/coordinates/14400.api.rst` (the number is a placeholder to be renamed to the PR number).
- Behaviour change: names are case-sensitive and stay strict rather than normalized, so a misconfiguration is surfaced instead of guessed.
