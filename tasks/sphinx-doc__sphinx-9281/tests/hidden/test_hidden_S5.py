from jinja2 import Environment

from sphinx.util.template import SphinxTemplateLoader


def test_first_configured_template_directory_takes_precedence(tmp_path):
    preferred = tmp_path / 'preferred'
    legacy = tmp_path / 'legacy'
    system = tmp_path / 'system'
    for directory in (preferred, legacy, system):
        directory.mkdir()

    (preferred / 'page.html').write_text('Current branding', encoding='utf-8')
    (legacy / 'page.html').write_text('Legacy branding', encoding='utf-8')
    (system / 'page.html').write_text('Default branding', encoding='utf-8')

    loader = SphinxTemplateLoader(
        confdir=str(tmp_path),
        templates_paths=['preferred', 'legacy'],
        system_templates_paths=[str(system)],
    )
    environment = Environment(loader=loader)

    assert environment.get_template('!page.html').render() == 'Default branding'
    assert environment.get_template('page.html').render() == 'Current branding'
