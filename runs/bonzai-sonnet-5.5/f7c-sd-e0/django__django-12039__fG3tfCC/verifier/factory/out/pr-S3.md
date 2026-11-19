Fix template backends searching app template dirs before DIRS

`BaseEngine.template_dirs` built its list as `app dirs + DIRS`, so for backends that use it (Jinja2, and the dummy `TemplateStrings` backend) a template bundled in an installed app shadowed a project template of the same name in `DIRS`. Projects overriding bundled templates (e.g. custom receipt email templates) got the bundled branding back. The DjangoTemplates backend was unaffected (its loaders already search DIRS first).

Fix: append app dirs after DIRS (`template_dirs += get_app_template_dirs(self.app_dirname)`).

Tests: added `test_dirs_precede_app_dirs` for the Jinja2 and dummy backends; both fail before the change and pass after. `template_backends` and `template_tests` pass, except `test_loaders.test_permissions_error`, which fails because the sandbox runs as root (unrelated).

Command: `cd tests && python runtests.py --parallel=1 template_backends.test_jinja2 template_backends.test_dummy` (jinja2 must be installed)
