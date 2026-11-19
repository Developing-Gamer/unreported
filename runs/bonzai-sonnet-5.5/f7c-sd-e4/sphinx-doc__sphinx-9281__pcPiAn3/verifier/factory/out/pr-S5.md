Fix autosummary searching templates_path in reverse order

**Problem**: Generated autosummary pages (module/class) could use an old template (e.g. old branding) while the other pages used the current one, even after clean rebuilds.

**Cause**: `SphinxTemplateLoader.__init__` did `self.loaders.insert(0, loader)` for each `templates_path` entry, reversing their precedence. With same-named templates in several directories the last one won, unlike the HTML builder where the first wins.

**Fix**: use `self.loaders.append(loader)` so earlier `templates_path` entries take precedence and system templates remain last. Added `test_SphinxTemplateLoader_precedence` (fails before: returned `from second`) and a CHANGES entry.

**Verification**: `python -m pytest tests/test_util_template.py tests/test_ext_autosummary.py tests/test_templating.py` -> 29 passed.
