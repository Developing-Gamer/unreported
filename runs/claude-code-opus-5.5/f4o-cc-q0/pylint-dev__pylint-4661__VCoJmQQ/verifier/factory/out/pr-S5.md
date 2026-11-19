Fix missing-raises-doc false positive for multi-dot qualified exception names

## Root cause
`DocstringParameterChecker.visit_raise` (pylint/extensions/docparams.py) reduces documented exception names to their class name before comparing them with the raised exceptions. It used `exc.split(".", 1)[-1]`, which strips only the first component. `re.error` became `error`, but `mypackage.errors.ValueError` became `errors.ValueError`. That never matched `ValueError`, so `"ValueError" not documented as being raised` was reported even though the docstring lists it.

## Change
Use `exc.split(".")[-1]` so the comparison uses the last component, which is the class name, as the code comment says.

## Verification
- Added `test_find_google_raises_deeply_qualified_exc` and `test_find_sphinx_raises_deeply_qualified_exc` to `tests/extensions/test_check_raise_docs.py`. Both fail without the fix and pass with it.
- `pytest tests/extensions` passes.
