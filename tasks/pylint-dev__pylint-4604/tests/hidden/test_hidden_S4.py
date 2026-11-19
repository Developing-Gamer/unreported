import astroid

from pylint.checkers.refactoring.not_checker import NotChecker
from pylint.testutils import UnittestLinter


def test_set_on_right_preserves_partial_ordering_exemption():
    module = astroid.parse('''
class TagSet(set):
    pass

selected = TagSet({1})
result = not selected <= {2}
''')
    node = next(module.nodes_of_class(astroid.UnaryOp))
    linter = UnittestLinter()
    checker = NotChecker(linter)

    checker.visit_unaryop(node)

    messages = linter.release_messages()
    assert messages == [], (
        "A negated subset comparison must not be simplified to a strict "
        "superset comparison: these differ for incomparable sets. "
        f"Unexpected messages: {messages!r}"
    )
