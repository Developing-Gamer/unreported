Raise on invalid Sesame database setting instead of silently using 'all'

## Problem
`sesame_database.validate` replaced any value outside `all/simbad/ned/vizier` with `'all'` without error or warning. A setting like `'SIMBAD'`, `' ned '` or a typo (`'sinbad'`) made `get_icrs_coordinates` query every database (Sesame option `A`) and take the first listed position, so ambiguous names could resolve to different positions while the lookup still reported success.

## Fix
- Strip and lowercase string values, so `'SIMBAD'` -> `'simbad'`.
- Raise `ValueError` naming the allowed values for anything else.
- Offline tests in `test_name_resolve.py` (normalisation and invalid values); they fail on the previous code (7 failures) and pass now.
- Changelog entry `docs/changes/coordinates/14600.api.rst` (number is a placeholder to be renamed to the real PR number).

## Verification
`pytest astropy/coordinates/tests/test_name_resolve.py -k sesame_database`
