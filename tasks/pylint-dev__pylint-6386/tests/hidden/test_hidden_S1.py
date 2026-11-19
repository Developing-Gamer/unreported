import pytest

from pylint.message.message_id_store import MessageIdStore


@pytest.mark.parametrize("legacy_name", ["W9000", "w9000", "old-combined-warning"])
def test_legacy_name_keeps_all_replacement_messages(legacy_name):
    store = MessageIdStore()
    store.register_message_definition(
        "W9001", "first-warning", [("W9000", "old-combined-warning")]
    )
    store.register_message_definition(
        "W9002", "second-warning", [("W9000", "old-combined-warning")]
    )

    assert store.get_active_msgids("first-warning") == ["W9001"]
    assert store.get_active_msgids("second-warning") == ["W9002"]
    assert store.get_active_msgids(legacy_name) == ["W9001", "W9002"]
