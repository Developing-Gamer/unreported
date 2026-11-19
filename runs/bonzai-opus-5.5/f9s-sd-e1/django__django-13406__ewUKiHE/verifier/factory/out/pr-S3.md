Fix QuerySet.query setter losing values() result shape for pickled queries

## Overview
Pickling `qs.query` of a `values()`/`values().annotate()` queryset and assigning it to a fresh queryset (`qs.query = pickle.loads(...)`) returned broken model instances instead of dicts; accessing `.id` raised AttributeError. The result shape was stored only on the QuerySet (`_iterable_class`), not on the Query.

## Details
- `QuerySet.query` setter now sets `_iterable_class = ValuesIterable` when the assigned query has `values_select`, so the selected columns come back as dicts.
- Tests in `tests/queryset_pickle/tests.py` reload a pickled `values('name')` and `values('name').annotate(count=Count('id'))` query. Before the fix they fail with `AttributeError: 'NoneType' object has no attribute 'attname'`.
- Limitation: a query carries no tuple/flat information, so a reloaded `values_list()` query yields dicts, not tuples.

## Verification
`python tests/runtests.py queryset_pickle queries aggregation aggregation_regress` - 569 tests OK.
