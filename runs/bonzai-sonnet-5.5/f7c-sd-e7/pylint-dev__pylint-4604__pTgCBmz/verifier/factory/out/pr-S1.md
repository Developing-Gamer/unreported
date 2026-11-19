Fix pyreverse --ignore= being overridden by the default CVS ignore

## Overview
`pyreverse --ignore=` (an explicitly empty exclusion list) still skipped any package or directory named `CVS`, so a legacy `CVS` package silently vanished from the diagrams. An empty ignore list now excludes nothing.

## Cause
`Run.run` passed `black_list=self.config.ignore_list or ("CVS",)`. An explicit empty value parses to an empty (falsy) list, so `or` replaced it with `("CVS",)`. The fallback was redundant: the `--ignore` option already defaults to `("CVS",)`.

## Changes
- `pylint/pyreverse/main.py`: pass `self.config.ignore_list` directly.
- `tests/unittest_pyreverse_main.py`: new tests building a package with a `CVS` subpackage. Default run still excludes it; `--ignore=` includes it.
- `ChangeLog` entry.

## Proof
Before: `python -m pytest tests/unittest_pyreverse_main.py` -> `test_empty_ignore_list_does_not_skip_cvs` fails (`'legacy_pkg.CVS.old_module' in dict_keys(['legacy_pkg', 'legacy_pkg.current'])`). After: all pyreverse tests pass.

## Verification
`python -m pytest tests/unittest_pyreverse_main.py tests/unittest_pyreverse_diadefs.py tests/unittest_pyreverse_inspector.py tests/unittest_pyreverse_writer.py`
