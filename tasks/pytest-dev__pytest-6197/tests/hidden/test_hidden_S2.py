import pytest
from _pytest.nodes import Node


def test_prepended_skip_marker_takes_precedence(request):
    node = Node("example", parent=request.session)
    node.add_marker(pytest.mark.skip(reason="default environment policy"))
    node.add_marker(pytest.mark.xfail(reason="known intermittent failure"))
    node.add_marker(
        pytest.mark.skip(reason="case-specific environment policy"),
        append=False,
    )

    marker = node.get_closest_marker("skip")
    assert marker.kwargs["reason"] == "case-specific environment policy"
