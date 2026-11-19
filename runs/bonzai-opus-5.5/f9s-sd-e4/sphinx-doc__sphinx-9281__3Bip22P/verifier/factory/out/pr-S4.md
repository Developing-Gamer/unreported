C domain: parse `:type:` info fields as C expressions (fixes #8945)

## Overview
Documenting a function-like macro with typed arguments, e.g. `.. c:macro:: BOB_CATCH_FUNCTION(char* message, void* ret)`, is not accepted since 3.0 (macro parameters are plain identifiers, intentionally). The supported alternative, `:param:`/`:type:` fields, also warned: `:type message: char*` produced `Unparseable C cross-reference: 'char*'`, because type fields were turned into a `pending_xref` of role `type`, which only accepts (nested) names, not builtin types or pointers. Type fields of C directives are now rendered through the C domain's `expr` role, so `char*`, `void*`, `unsigned int`, etc. build without warnings.

## Details
- `sphinx/util/docfields.py`: `Field.make_xref`/`make_xrefs` and the `make_field` methods take optional `inliner` and `location`. When given and the domain has a role of the requested name, that role is run on the target instead of creating a bare `pending_xref`. `DocFieldTransformer` passes the inliner and the field list node. Without an inliner, behaviour is unchanged.
- `sphinx/domains/c.py`: `:type:` fields of `CObject` use `typerolename='expr'`.
- `sphinx/domains/python.py`: the Python field classes accept the new arguments but never run a role (they always need a `pending_xref` for `refspecific` handling), so Python output is unchanged.
- Docs: `c:macro` now says that arguments are identifiers only and types go into `:param:`/`:type:` fields. CHANGES entry added.
- The macro parameter error message is left as is.
- Risk: third-party `Field` subclasses overriding `make_xref` with the old signature will receive the two new arguments (same as upstream Sphinx 4.1).

## Verification
- New test `tests/test_domain_c.py::test_build_domain_c_typed_fields` fails on the base commit (`Unparseable C cross-reference: 'char*'`, plus `c:type reference target not found: int`) and passes with the fix.
- Full suite: 1687 passed, 5 failed (`test_ext_imgconverter`, `test_ext_viewcode`, 2 in `test_intl`, `test_util_i18n::test_format_date`); the same 5 fail on the base commit (environment-related).
