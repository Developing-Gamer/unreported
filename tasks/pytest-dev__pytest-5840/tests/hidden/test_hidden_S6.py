from io import StringIO
from types import SimpleNamespace

import _pytest.config
import _pytest.pastebin as pastebin


def test_failure_paste_link_identifies_innermost_frame(monkeypatch):
    outer_location = "tests/test_job.py:12: in test_job"
    inner_location = "pkg/job.py:34: AssertionError"
    traceback_text = "tests/test_job.py:12: in test_job\npkg/job.py:34: AssertionError\n"
    report = SimpleNamespace(
        longrepr=SimpleNamespace(
            reprtraceback=SimpleNamespace(
                reprentries=[
                    SimpleNamespace(reprfileloc=outer_location),
                    SimpleNamespace(reprfileloc=inner_location),
                ]
            )
        ),
        toterminal=lambda tw: tw.write(traceback_text),
    )

    buffer = StringIO()
    writer = SimpleNamespace(stringio=buffer, write=buffer.write)
    monkeypatch.setattr(
        _pytest.config,
        "create_terminal_writer",
        lambda config, stringio: writer,
    )

    uploaded = []
    paste_url = "https://bpaste.net/show/abc123"

    def create_paste(contents):
        uploaded.append(contents)
        return paste_url

    monkeypatch.setattr(pastebin, "create_new_paste", create_paste)
    lines = []
    reporter = SimpleNamespace(
        config=SimpleNamespace(option=SimpleNamespace(pastebin="failed")),
        stats={"failed": [report]},
        write_sep=lambda *args: None,
        write_line=lines.append,
    )

    pastebin.pytest_terminal_summary(reporter)

    assert uploaded == [traceback_text]
    assert lines == ["{} --> {}".format(inner_location, paste_url)]
