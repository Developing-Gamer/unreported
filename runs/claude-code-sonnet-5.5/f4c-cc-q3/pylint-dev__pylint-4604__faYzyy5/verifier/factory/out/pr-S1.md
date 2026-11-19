pyreverse: respect an empty --ignore list instead of always ignoring CVS

Root cause: `pylint/pyreverse/main.py` called `project_from_files(..., black_list=self.config.ignore_list or ("CVS",))`. An empty ignore list is falsy, so it was replaced with `("CVS",)`. A package or directory named `CVS` was therefore dropped from the diagrams even when the user explicitly asked to ignore nothing. The option already defaults to `("CVS",)`, so the fallback was redundant.

Change: pass `self.config.ignore_list` straight through. The default is unchanged.

Verification: added `tests/unittest_pyreverse_main.py`. The empty-list test fails before the change and passes after it. The unittest_pyreverse_* tests also pass.
