Fix QuerySet.query setter so pickled values()/annotate() queries return dicts

## Overview
Assigning a pickled `values('x').annotate(...)` query to a fresh queryset (as documented in "Pickling QuerySets") returned broken model instances instead of dicts: the SQL selected only the values columns, but the queryset still used `ModelIterable`, so accessing attributes such as `.id` raised `AttributeError`.

## Details
The `QuerySet.query` setter now switches `_iterable_class` to `ValuesIterable` when the assigned query has `values_select`. Regression test added in `tests/queryset_pickle/tests.py` (`test_values_queryset_from_pickled_query`); it failed before with `AttributeError: 'NoneType' object has no attribute 'attname'` and passes now.

Limitation: `values_list()` queries are returned as dicts as well, since the query alone does not record the row format.

## Verification
`cd tests && PYTHONPATH=/testbed python runtests.py queryset_pickle queries expressions_case annotations --parallel 1` — OK.
