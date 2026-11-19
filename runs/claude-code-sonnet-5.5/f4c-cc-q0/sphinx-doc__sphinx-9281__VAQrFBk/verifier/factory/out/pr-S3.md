autodoc: render Enum default values as `MyEnum.A` instead of `<MyEnum.A: 10>`

Root cause: `sphinx.util.inspect.object_description()` falls back to `repr()` for
arbitrary objects. For `enum.Enum` members `repr()` is `<MyEnum.ValueA: 10>`,
so function signatures such as `def f(e: MyEnum = MyEnum.ValueA)` were rendered
with the ugly angle-bracket form (issue S3).

Change: `object_description()` now returns `"<ClassName>.<member name>"` for
`enum.Enum` instances. Added a CHANGES entry and `test_enum_description` in
`tests/test_util_inspect.py`.

Verification: `pytest tests/test_util_inspect.py` passes (39 + new test). Nested
containers still use their own `repr()`; that is unchanged.
