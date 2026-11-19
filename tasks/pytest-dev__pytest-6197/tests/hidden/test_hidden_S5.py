import pytest


def test_banner_includes_headers_from_multiple_plugins(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("PYTEST_DISABLE_PLUGIN_AUTOLOAD", "1")
    monkeypatch.delenv("PYTEST_ADDOPTS", raising=False)
    monkeypatch.delenv("PYTEST_PLUGINS", raising=False)

    config_file = tmp_path / "pytest.ini"
    config_file.write_text("[pytest]\n", encoding="utf-8")
    test_file = tmp_path / "test_sample.py"
    test_file.write_text("def test_sample():\n    pass\n", encoding="utf-8")

    class BuildHeader:
        def pytest_report_header(self, config):
            return ["build-metadata: build-2417"]

    class RuntimeHeader:
        def pytest_report_header(self, config):
            return ["runtime-metadata: worker-linux"]

    exit_code = pytest.main(
        [
            "-v",
            "--color=no",
            "-c", str(config_file),
            "--confcutdir", str(tmp_path),
            str(test_file),
        ],
        plugins=[BuildHeader(), RuntimeHeader()],
    )
    output = capsys.readouterr().out

    assert exit_code == 0, output
    assert "build-metadata: build-2417" in output, output
    assert "runtime-metadata: worker-linux" in output, output
