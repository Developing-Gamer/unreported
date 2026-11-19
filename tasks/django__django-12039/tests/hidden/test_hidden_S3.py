from pathlib import Path

from django.template.backends import base


class AppTemplateEngine(base.BaseEngine):
    app_dirname = 'templates'


def test_explicit_template_directory_overrides_app_templates(tmp_path, monkeypatch):
    overrides = tmp_path / 'overrides'
    packaged = tmp_path / 'packaged'
    overrides.mkdir()
    packaged.mkdir()
    (overrides / 'receipt.html').write_text('Custom receipt', encoding='utf-8')
    (packaged / 'receipt.html').write_text('Default receipt', encoding='utf-8')

    monkeypatch.setattr(
        base, 'get_app_template_dirs', lambda dirname: (str(packaged),)
    )
    engine = AppTemplateEngine({
        'NAME': 'receipts',
        'DIRS': [str(overrides)],
        'APP_DIRS': True,
    })

    selected = next(
        Path(filename)
        for filename in engine.iter_template_filenames('receipt.html')
        if Path(filename).is_file()
    )
    assert selected.read_text(encoding='utf-8') == 'Custom receipt'
