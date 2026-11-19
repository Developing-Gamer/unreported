Fix OptionsProviderMixIn.options_and_values returning all options for an empty selection

## Problem
The report lists every setting when no settings are selected; selecting one gives the expected single entry.

## Cause
`OptionsProviderMixIn.options_and_values(options=None)` used `if not options:`, so an empty selection (`[]`) was treated like "nothing passed" and fell back to `self.options`. `_ArgumentsProvider.options_and_values` already uses `is None`.

## Fix
Use `if options is None:` so only an omitted argument means "all options".

## Verification
- New test `tests/config/test_deprecations.py::test_options_provider_mixin_options_and_values_selection` (None -> all, `[]` -> none, one option -> one). Fails before the fix, passes after.
- `pytest tests/config`: 72 passed.
