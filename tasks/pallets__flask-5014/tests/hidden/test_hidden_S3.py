import warnings

import flask.globals as flask_globals
from flask import Flask, has_request_context


def test_legacy_request_stack_is_empty_in_app_only_context():
    app = Flask(__name__)

    with app.app_context():
        assert not has_request_context()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            request_active = flask_globals._request_ctx_stack.top is not None

        assert request_active is False
