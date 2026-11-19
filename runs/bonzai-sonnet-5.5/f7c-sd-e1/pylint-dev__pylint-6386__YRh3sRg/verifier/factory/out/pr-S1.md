Fix disabling an old message name shared by several messages (missing-docstring / C0111)

## Problem
`disable=missing-docstring` (or `C0111`) used to silence all three docstring warnings. Now `missing-module-docstring` (C0114) and `missing-class-docstring` (C0115) still show up; only C0116 is silenced.

## Cause
`MessageIdStore.add_legacy_msgid_and_symbol` did `self.__old_names[msgid] = [new_msgid]`, overwriting the list each time a message re-declared the same old name. Only the last registered message survived.

## Fix
Append to the list (`setdefault` + de-duplicated append) so the old name resolves to every current message.

## Verification
- New unit test `tests/message/unittest_message_id_store.py::test_legacy_msgid_shared_by_several_messages` fails before the change (get_active_msgids('C0111') returned only ['C0116']) and passes after.
- `pytest tests/message tests/lint`: 90 passed.
- `pylint --disable=C0111` on a module with no docstrings: no docstring messages.
- ChangeLog entry added.
