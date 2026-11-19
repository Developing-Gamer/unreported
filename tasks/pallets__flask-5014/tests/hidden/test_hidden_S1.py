from flask import Flask, session, stream_with_context


def test_cleared_session_stays_empty_in_streamed_response():
    app = Flask(__name__)
    app.config.update(TESTING=True, SECRET_KEY="streaming-session-test")

    @app.route("/sign-in")
    def sign_in():
        session["user"] = "alice"
        return "signed in"

    @app.route("/sign-out")
    def sign_out():
        session.clear()

        @stream_with_context
        def generate():
            yield session.get("user", "anonymous")

        return app.response_class(generate(), mimetype="text/plain")

    client = app.test_client()
    assert client.get("/sign-in").status_code == 200

    response = client.get("/sign-out", buffered=True)
    assert response.status_code == 200
    assert response.get_data(as_text=True) == "anonymous"
