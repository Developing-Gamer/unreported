import astroid
import pytest

from pylint.extensions.docparams import DocstringParameterChecker
from pylint.testutils import CheckerTestCase


class TestQualifiedRaisesDocumentation(CheckerTestCase):
    CHECKER_CLASS = DocstringParameterChecker

    @pytest.mark.parametrize(
        "documented_name",
        ["ValueError", "errors.ValueError", "acme.errors.ValueError"],
    )
    def test_documented_exception_class_is_recognized(self, documented_name):
        node = astroid.extract_node(
            f'''
def validate():
    """Validate the payload.

    :raises {documented_name}: If the payload is invalid.
    """
    raise ValueError("invalid payload")  #@
'''
        )
        with self.assertNoMessages():
            self.checker.visit_raise(node)
