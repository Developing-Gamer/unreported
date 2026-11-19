autodoc: render Enum default values as `MyEnum.ValueA` instead of `<MyEnum.ValueA: 10>`

## Root cause

When autodoc builds a function signature, it formats default values with
`sphinx.util.inspect.object_description()`. That function handled dicts, sets
and frozensets specially and used `repr()` for everything else. For `enum.Enum`
members, `repr()` returns `<MyEnum.ValueA: 10>`, so signatures came out as
`ugly_enum_func(e: ugly_enum.MyEnum = <MyEnum.ValueA: 10>) -> None`.

## Change

- `sphinx/util/inspect.py`: `object_description()` now returns
  `ClassName.member_name` for `enum.Enum` instances. The result is
  `MyEnum.ValueA`, which is also what you would write in source code.
- `tests/test_util_inspect.py`: added `test_object_description_enum` and
  `test_signature_with_enum_default`. The second one checks
  `stringify_signature()` from start to finish for a function with an Enum
  default.
- `CHANGES`: added a bug-fix entry.

## Verification

- Both new tests fail without the change (they get `<MyEnum.FOO: 1>` /
  `<MyEnum.ValueA: 10>`) and pass with it.
- `pytest tests/test_util_inspect.py tests/test_ext_autodoc*.py`: 205 passed.
