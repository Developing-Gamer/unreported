Don't add an extra '*' when tab-completing prefixes that already contain glob wildcards

## Root cause
`FastFilesCompleter.__call__` in `src/_pytest/_argcomplete.py` used `if "*" not in prefix or "?" not in prefix:` to decide whether to add `*` to the prefix. That is true unless the prefix contains both wildcards. So a pattern like `test_*.py` became `test_*.py*` and also matched files such as `test_foo.py.bak`.

## Change
Changed `or` to `and`, so `*` is added only when the prefix has no wildcard.

## Verification
- Added `TestArgComplete::test_wildcard_prefix_not_extended` in `testing/test_argcomplete.py`. `test_*.py` and `test_?oo.py` complete only to `test_foo.py`, and an ordinary prefix still completes to both files. The test fails before the change and passes after.
- `testing/test_argcomplete.py` passes.
