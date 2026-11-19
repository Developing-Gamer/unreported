from collections import Counter

from pylint.testutils.lint_module_test import LintModuleTest


def test_multiset_difference_preserves_unexpected_message_counts():
    expected = Counter({
        (12, "unused-import"): 1,
        (18, "undefined-variable"): 1,
    })
    actual = Counter({
        (12, "unused-import"): 3,
        (23, "unused-variable"): 1,
    })

    missing, unexpected = LintModuleTest.multiset_difference(expected, actual)

    assert missing == Counter({(18, "undefined-variable"): 1})
    assert unexpected == {
        (12, "unused-import"): 2,
        (23, "unused-variable"): 1,
    }
