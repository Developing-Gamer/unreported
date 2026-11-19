Fix pyreverse ignoring an explicit empty --ignore= list

## Overview
`pyreverse --ignore=` (an explicit empty exclusion list) still skipped packages named `CVS`, so a legacy sub-package silently vanished from the generated diagrams while the export reported success. `Run.run()` used `self.config.ignore_list or ("CVS",)`, and an empty list is falsy so it was replaced by the default.

## Details
- `pylint/pyreverse/main.py`: pass `self.config.ignore_list` straight to `project_from_files`. The `--ignore` option already defaults to `("CVS",)`, so behaviour without the option is unchanged.
- `tests/unittest_pyreverse_inspector.py`: regression test running `pyreverse --ignore= -o dot` on a package with a `CVS` sub-package; asserts its class appears in `classes_proj.dot`.
- ChangeLog entry.

## Verification
- New test fails before the fix (`Legacy` missing from the dot output) and passes after.
- `pytest unittest_pyreverse_inspector.py unittest_pyreverse_writer.py unittest_pyreverse_diadefs.py` passes.
