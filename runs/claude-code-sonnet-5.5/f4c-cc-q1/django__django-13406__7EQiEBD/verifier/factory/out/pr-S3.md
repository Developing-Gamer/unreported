Use ValuesIterable when a values() query is assigned to a QuerySet

Root cause: `QuerySet.query` setter only stored the query. The iterable class (ValuesIterable vs ModelIterable) lives on the queryset, so assigning an unpickled values()/values_list() query to a fresh queryset yielded broken model instances instead of dicts.

Change: the setter in django/db/models/query.py sets `_iterable_class = ValuesIterable` when `value.values_select` is non-empty. Added `test_values_queryset_from_pickled_query` in tests/queryset_pickle/tests.py.

Verification: ran queryset_pickle, utils_tests.test_dateformat, model_enums and template_tests.test_custom; the new test errors without the fix and passes with it.
