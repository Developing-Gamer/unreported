autodoc: render Enum members used as default values as `MyEnum.ValueA`

## Overview
Signatures with an Enum member as a parameter default were rendered with the raw repr, e.g. `e: MyEnum = <MyEnum.ValueA: 10>`. They now render `e: MyEnum = MyEnum.ValueA`.

## Cause
`stringify_signature` formats defaults with `sphinx.util.inspect.object_description()`, which special-cased dict/set/frozenset and otherwise used `repr()`. The repr of an Enum member is `<MyEnum.ValueA: 10>`.

## Change
- `object_description()` returns `ClassName.member_name` for `enum.Enum` instances.
- Added `test_enum_description` in `tests/test_util_inspect.py` (fails before the fix, passes after).
- CHANGES entry.

## Verification
`pytest tests/test_util_inspect.py tests/test_ext_autodoc.py tests/test_ext_autodoc_configs.py`: 135 passed.
