Fix old message names that map to several new messages only disabling the last one

## Overview
When several messages share one old name (e.g. `C0111`/`missing-docstring` → `C0114`, `C0115`, `C0116`), an existing `disable=missing-docstring` entry only silenced the last registered message, so CI kept showing the other warnings without any config change. The old name now resolves to all of its new messages again.

## Details
`MessageIdStore.add_legacy_msgid_and_symbol` did `self.__old_names[msgid] = [new_msgid]`, overwriting the list on each registration. It now appends the new msgid to the existing list (skipping duplicates), so `get_active_msgids("missing-docstring")` returns `['C0114', 'C0115', 'C0116']`.

The cache logic in `get_active_msgids` is unchanged; registration happens before lookups.

## Proof
- Before: `pytest tests/message/unittest_message_definition_store.py::test_multiple_child_of_old_name` fails with `assert 1 == 2 where 1 = len([MessageDefinition:child-two (W1236)])`.
- After: it passes; all of `tests/message` passes (33 passed).
- With the real checkers registered, `get_active_msgids("missing-docstring")` and `get_active_msgids("C0111")` both return `['C0114', 'C0115', 'C0116']`.

## Verification
`python -m pytest tests/message -q`
