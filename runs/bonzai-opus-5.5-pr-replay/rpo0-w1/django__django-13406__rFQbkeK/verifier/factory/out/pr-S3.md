Fix QuerySet.query setter losing values()/values_list() result shape

## Overview
Pickling `qs.query` for a `values()`/`values_list()` queryset and assigning it to a fresh queryset (`qs.query = pickled`) returned broken model instances (no pk; `.id` raised AttributeError) instead of dicts.

## Cause
`values()` records the result shape only on the QuerySet (`_iterable_class = ValuesIterable`), not on the Query. A fresh queryset keeps `ModelIterable`, so selected columns/aggregates were turned into model instances.

## Fix
In the `QuerySet.query` setter, set `_iterable_class = ValuesIterable` when `value.values_select` is non-empty.

## Tests
New `test_query_pickled_values` in `tests/queryset_pickle/tests.py` (values, values_list, values + annotate). Before: `AttributeError: 'NoneType' object has no attribute 'attname'`. After: passes.
Ran `cd tests && PYTHONPATH=/testbed python runtests.py queryset_pickle queries aggregation aggregation_regress --parallel 1`: 568 tests OK.
Note: a values_list query reassigned this way yields dicts (the query alone doesn't record tuple/flat).
