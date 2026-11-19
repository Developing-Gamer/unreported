import pytest

from _pytest._argcomplete import FastFilesCompleter


@pytest.mark.parametrize("pattern", ["test_?.py", "test_*.py"])
def test_wildcard_completion_preserves_extension_boundary(tmp_path, monkeypatch, pattern):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "test_a.py").write_text("")
    (tmp_path / "test_a.py.bak").write_text("")

    assert FastFilesCompleter()(pattern) == ["test_a.py"]
