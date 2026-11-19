Fix missing-raises-doc false positive for dotted exception names

Root cause: `DocstringParameterChecker.visit_raise` reduced documented exception names with `exc.split(".", 1)[-1]`, which only strips the first component: `pkg.mod.ValueError` became `mod.ValueError` and never matched `ValueError`.

Change: use `exc.rsplit(".", 1)[-1]` (pylint/extensions/docparams.py).

Verification: added `test_ignores_qualified_exception_names_in_raises_doc` (Sphinx and Google styles) in tests/extensions/test_check_docs.py; it fails before and passes after, and the rest of the suite is unchanged (only the pre-existing `recursion_error_3152` failure remains).
