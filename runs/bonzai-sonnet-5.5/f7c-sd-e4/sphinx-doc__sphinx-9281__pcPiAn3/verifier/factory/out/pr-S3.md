Fix rendering of Enum default values in signatures

**Problem**: Enum members used as parameter defaults were rendered via `repr()`, e.g. `<MyEnum.ValueA: 1>`, instead of `MyEnum.ValueA`.

**Cause**: `sphinx.util.inspect.object_description` special-cased dict/set/frozenset only; everything else fell to `repr()`. `stringify_signature` uses it for every default.

**Fix**: add an `enum.Enum` branch returning `ClassName.member`. Added `test_enum_object_description` (failed before, passes after) and a CHANGES entry.

**Verification**: `python -m pytest tests/test_util_inspect.py tests/test_ext_autodoc.py tests/test_ext_autodoc_configs.py tests/test_domain_py.py` -> 181 passed.
