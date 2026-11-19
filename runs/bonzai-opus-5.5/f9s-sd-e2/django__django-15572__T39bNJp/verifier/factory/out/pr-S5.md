Fixed Node.add() squashing an OR group into an AND parent with a single child

## Overview
`Q(is_active=True) & (Q(email=True) | Q(sms=True))` produced `(AND: is_active, email, sms)`, so a saved search for active customers with email OR SMS enabled only returned customers with both. `Node.add()` decided to squash the incoming node into `self` when `len(self) == 1` instead of `len(data) == 1`, which dropped the OR group. It now keeps the group: the result is `(AND: ('is_active', True), (OR: ('email', True), ('sms', True)))`.

## Details
- `django/utils/tree.py`: the squash condition checks the length of the node being added (`len(data) == 1`, where the connector is irrelevant), not of `self`.
- `tests/utils_tests/test_tree.py`: tests that a multi-child group with a different connector is kept, and that a single-child group is still squashed.

## Verification
- Before the fix, `test_add_mixed_connector_keeps_child_group` fails (`(AND: ('a', 1), ('b', 1), ('c', 1))` instead of the nested OR group).
- `cd tests && PYTHONPATH=/testbed python runtests.py --parallel 1 utils_tests.test_tree queries expressions`: 641 tests, OK.
