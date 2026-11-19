import sys

import pytest

from pylint.pyreverse import main


def test_empty_ignore_list_includes_normally_excluded_package(tmp_path, monkeypatch):
    package = tmp_path / "diagram_sample"
    package.mkdir()
    (package / "__init__.py").write_text(
        "class RootModel:\n    pass\n", encoding="utf-8"
    )
    legacy_package = package / "CVS"
    legacy_package.mkdir()
    (legacy_package / "__init__.py").write_text(
        "class ArchivedRecord:\n    pass\n", encoding="utf-8"
    )
    output = tmp_path / "diagrams"
    output.mkdir()

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(main, "insert_default_options", lambda: None)
    arguments = [
        "--ignore=",
        "--output=dot",
        "--output-directory=" + str(output),
        str(package),
    ]
    monkeypatch.setattr(sys, "argv", ["pyreverse"] + arguments)

    with pytest.raises(SystemExit) as result:
        main.Run(arguments)
    assert result.value.code == 0

    diagrams = "\n".join(
        path.read_text(encoding="utf-8") for path in output.glob("*.dot")
    )
    assert "RootModel" in diagrams
    assert "ArchivedRecord" in diagrams
