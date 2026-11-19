Fix Node.add squashing a nested OR group into an AND parent (Q(a) & (Q(b) | Q(c)))

## Overview
A saved search for active customers with email OR SMS enabled started returning only customers with both enabled. `Q(active=True) & (Q(email=True) | Q(sms=True))` was flattened to `active AND email AND sms`, losing the OR group.

## Details
`Node.add` in `django/utils/tree.py` decided whether to squash a child node into itself with `len(self) == 1`, but its own comment says the check is on the length of the *other* node (`data`). When the parent had one child, any child group was merged regardless of connector, so the nested OR connector was dropped (and likewise `Q(b) | (Q(a) & Q(c))` lost its AND group). Changed the check to `len(data) == 1` and removed the stale comment sentence.

Tests added in `tests/queries/test_q.py`: `test_combine_keeps_nested_or_group` and `test_combine_keeps_nested_and_group`. Before the fix they fail (`AssertionError: 3 != 2`).

## Verification
`cd tests && PYTHONPATH=/testbed python runtests.py queries utils_tests expressions lookup or_lookups null_queries --parallel 1` passes except `utils_tests.test_dateparse` `test_parse_date`/`test_parse_time`, which fail identically on the base commit.
