import requests


def test_head_honors_explicit_redirect_opt_in(monkeypatch):
    observed = {}
    response = object()

    def record_request(self, method, url, **kwargs):
        observed.update(kwargs)
        return response

    monkeypatch.setattr(requests.sessions.Session, 'request', record_request)

    result = requests.head(
        'http://monitor.example/health', allow_redirects=True
    )

    assert result is response
    assert observed['allow_redirects'] is True
