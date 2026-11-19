from io import StringIO

import django
from django.conf import settings
from django.core.management.commands.showmigrations import Command
from django.test.utils import override_settings


def test_filtered_plan_keeps_cross_app_prerequisites(tmp_path, monkeypatch):
    if not settings.configured:
        settings.configure(
            SECRET_KEY='migration-plan-test',
            INSTALLED_APPS=[],
            DATABASES={},
            USE_I18N=False,
        )
    django.setup()

    accounts = 'plan_test_accounts'
    orders = 'plan_test_orders'
    for app_label, dependencies in (
        (accounts, []),
        (orders, [(accounts, '0001_initial')]),
    ):
        package = tmp_path / app_label
        migrations = package / 'migrations'
        migrations.mkdir(parents=True)
        (package / '__init__.py').write_text('', encoding='utf-8')
        (migrations / '__init__.py').write_text('', encoding='utf-8')
        (migrations / '0001_initial.py').write_text(
            'from django.db import migrations\n\n'
            'class Migration(migrations.Migration):\n'
            '    dependencies = %r\n'
            '    operations = []\n' % dependencies,
            encoding='utf-8',
        )

    monkeypatch.syspath_prepend(str(tmp_path))
    with override_settings(
        INSTALLED_APPS=[accounts, orders],
        MIGRATION_MODULES={},
    ):
        output = StringIO()
        command = Command(stdout=output, no_color=True)
        command.verbosity = 1
        # A connection of None loads the real migration graph without a database.
        command.show_plan(None, [orders])

    assert output.getvalue().splitlines() == [
        '[ ]  plan_test_accounts.0001_initial',
        '[ ]  plan_test_orders.0001_initial',
    ]
