Restore values() results when a pickled values()/values_list() query is assigned to QuerySet.query

## Root cause
If you assign a query to a queryset (`qs.query = pickle.loads(pickle.dumps(other.query))`, as the pickling docs describe), only `_query` was replaced. The queryset kept its default `ModelIterable`, even though the query's `values_select` was set by `values()`/`values_list()`. Rows shaped for values, such as GROUP BY aggregates, were then turned into broken model instances, and accessing `.pk` raised `AttributeError: 'NoneType' object has no attribute 'attname'`.

## Change
In `django/db/models/query.py`, the `QuerySet.query` setter now switches `_iterable_class` to `ValuesIterable` when `value.values_select` is set. The iterable-class choice is not stored on the query, so a reloaded `values_list()` query returns dicts, which is the same as `values()`.

## Verification
- Added `test_annotation_values` and `test_annotation_values_list` (values_list plain, flat and named) in `tests/queryset_pickle/tests.py`. Both fail without the fix and pass with it.
- Ran `runtests.py queryset_pickle queries utils_tests.test_dateformat template_tests.test_custom model_enums`: 483 tests, OK.
