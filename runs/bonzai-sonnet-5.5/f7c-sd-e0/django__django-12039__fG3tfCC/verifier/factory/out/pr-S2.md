Fix showmigrations --plan <app> omitting cross-app dependencies

`showmigrations --plan <app>` computed each target's full dependency chain but then dropped every migration whose app was not one of the requested apps. Dependencies in other apps (e.g. an accounts migration that orders depends on) were missing from the per-app plan even though the full plan lists them ahead of the app's migrations.

Fix: in `show_plan`, list every migration in each target's dependency chain (`if migration not in seen:`); targets are still the leaf nodes of the requested apps.

Verification: `test_showmigrations_plan_single_app_label` and `test_showmigrations_plan_multiple_app_labels` failed before the change (book_app.0001_initial missing) and pass now; full `migrations.test_commands` passes.
Run: `cd tests && PYTHONPATH=/testbed python runtests.py migrations.test_commands.MigrateTests.test_showmigrations_plan_single_app_label migrations.test_commands.MigrateTests.test_showmigrations_plan_multiple_app_labels`
