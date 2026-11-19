Honor an empty-string id returned by pytest_make_parametrize_id

## Root cause
`_idval` in `src/_pytest/python.py` checked the hook result with `if hook_id:`. An empty string returned on purpose by `pytest_make_parametrize_id` was treated as "no answer", and pytest fell back to its default id. The hook spec says the hook returns `None` when it doesn't know about a value, and the hook is `firstresult`, which stops at the first non-None result. So `""` is a real answer, and pluggy already treats it as one.

## Change
Changed the check to `if hook_id is not None:`.

## Verification
- Added `TestMarkersWithParametrization::test_pytest_make_parametrize_id_empty_string` in `testing/python/metafunc.py`. The hook returns `""` for one argument, and the test checks that the collected id is `test_func[a-]`. It fails before the change (id `a-b`) and passes after.
- `testing/python/metafunc.py` passes.
