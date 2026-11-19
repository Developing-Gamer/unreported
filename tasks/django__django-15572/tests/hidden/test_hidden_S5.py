from django.utils.tree import Node


def _matches(expression, values):
    if not isinstance(expression, Node):
        return values[expression]
    children = [_matches(child, values) for child in expression.children]
    result = all(children) if expression.connector == "AND" else any(children)
    return not result if expression.negated else result


def test_adding_or_group_to_single_condition_preserves_alternatives():
    criteria = Node(children=["active"], connector="AND")
    contact_options = Node(
        children=["email_enabled", "sms_enabled"], connector="OR"
    )
    criteria.add(contact_options, "AND")

    assert _matches(
        criteria,
        {"active": True, "email_enabled": True, "sms_enabled": False},
    )
    assert _matches(
        criteria,
        {"active": True, "email_enabled": False, "sms_enabled": True},
    )
    assert not _matches(
        criteria,
        {"active": False, "email_enabled": True, "sms_enabled": True},
    )
