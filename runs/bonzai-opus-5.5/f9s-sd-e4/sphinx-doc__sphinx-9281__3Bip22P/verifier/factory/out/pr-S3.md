autodoc: render Enum default values in signatures as MyEnum.Member

## Overview
Enum members used as parameter defaults were rendered in autodoc signatures using their raw `repr()`, e.g. `<MyEnum.ValueA: 10>`. They now render as `MyEnum.ValueA`, as the issue expects.

## Details
`sphinx.util.inspect.object_description()` only special-cased dict/set/frozenset and otherwise fell back to `repr()`. `stringify_signature()` uses it for every default. Added an `enum.Enum` case returning `ClassName.member_name`. Added `test_enum_description` and a CHANGES entry.

## Verification
- Before: `tests/test_util_inspect.py::test_enum_description` fails (got `<MyEnum.ValueA: 10>`).
- After: passes; test_util_inspect, test_ext_autodoc, test_ext_autodoc_configs and test_domain_py: 181 passed.
