Fix values()/annotate() queryset crashing when its pickled query is assigned to a fresh queryset

## Overview
Assigning an unpickled `values()`/`annotate()` query (`qs.query = pickle.loads(...)`) to a new queryset returned broken model instances instead of dicts; accessing any field raised `AttributeError: 'NoneType' object has no attribute 'attname'`. The `QuerySet.query` setter now switches the queryset to `ValuesIterable` when the assigned query has `values_select`, so results are dicts as with the original queryset.

## Details
- Cause: the `query` setter only stored the query; `_iterable_class` stayed `ModelIterable`, which tried to build model instances from the values-only columns.
- Fix: in `django/db/models/query.py`, `if value.values_select: self._iterable_class = ValuesIterable`.
- Limitation: `values_list()`/`flat` shape is not recorded on the query, so such a query is returned as dicts (not tuples) when reassigned.
- Test: `queryset_pickle.tests.PickleabilityTestCase.test_values_queryset_from_pickled_query` (fails before with the AttributeError above, passes after).

## Verification
`cd tests && PYTHONPATH=/testbed python runtests.py queryset_pickle queries expressions_case annotations aggregation lookup --parallel=1` passes.
