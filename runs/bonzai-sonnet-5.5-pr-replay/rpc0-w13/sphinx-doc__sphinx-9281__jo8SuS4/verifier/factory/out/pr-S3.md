autodoc: render Enum default values in signatures as `MyEnum.member`

## Overview
Documented functions with an Enum member as a parameter default showed the raw repr, e.g. `e: MyEnum = <MyEnum.ValueA: 1>`. They now show `e: MyEnum = MyEnum.ValueA`, as the reporter expected.

## Details
`sphinx.util.inspect.object_description` special-cased dict/set/frozenset and otherwise fell back to `repr()`. `stringify_signature` uses it for every parameter default, so Enum members got Enum's repr. Added an `enum.Enum` branch returning `ClassName.member_name`. Added a CHANGES entry.

## Verification
- New test `tests/test_util_inspect.py::test_enum_description` failed before the fix and passes after.
- `pytest tests/test_util_inspect.py tests/test_ext_autodoc.py tests/test_ext_autodoc_configs.py tests/test_domain_py.py`: 181 passed.
