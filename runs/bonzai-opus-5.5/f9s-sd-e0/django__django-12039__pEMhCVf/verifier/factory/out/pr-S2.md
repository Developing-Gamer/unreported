Fix showmigrations --plan <app_label> hiding dependency migrations from other apps

## Overview
`showmigrations --plan orders` built the full dependency-ordered plan for the requested apps, then dropped every migration whose app was not named on the command line. A migration from another app (e.g. an accounts migration that orders depends on) that is still ahead of the app's migrations in the full plan was therefore missing from the app-scoped plan. The documentation says dependencies of the provided apps may also be included.

## Details
In `show_plan`, the extra `migration[0] in app_names` filter is removed. Targets are already restricted to the leaf nodes of the requested apps, so `forwards_plan` yields exactly those migrations plus their dependencies.

## Verification
- Before the fix, `test_showmigrations_plan_single_app_label` and `test_showmigrations_plan_multiple_app_labels` fail (`book_app.0001_initial` missing from the plan).
- After the fix: `cd tests && PYTHONPATH=/testbed python runtests.py migrations.test_commands` passes (90 tests).
