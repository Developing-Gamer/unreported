Fix OptionsProviderMixIn.options_and_values returning every option for an empty selection

## Overview
`OptionsProviderMixIn.options_and_values([])` returned all of the provider's options, because it used `if not options:` and so treated an explicitly empty selection like "no argument". An empty selection now yields nothing; omitting the argument still yields every option, and a one-option selection yields that option. This matches the newer `_ArgumentsProvider.options_and_values`, which checks `is None`.

## Details
- `pylint/config/options_provider_mixin.py`: `if not options:` -> `if options is None:`. Existing callers (`base_checker`, `utils/docs.py`, doc extension) pass no argument and are unaffected.
- Added `tests/config/test_options_provider_mixin.py`, which failed before the fix (`[]` selection yielded 2 items) and passes after.

## Verification
- `python -m pytest tests/config/test_options_provider_mixin.py -q -p no:warnings` (fails before, passes after)
- `python -m pytest tests/config tests/checkers/unittest_base_checker.py -q -p no:warnings`: 73 passed
