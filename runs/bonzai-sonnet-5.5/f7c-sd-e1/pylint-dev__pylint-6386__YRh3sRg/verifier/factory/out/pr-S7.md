Declare `--verbose`/`-v` and `--enable-all-extensions` as taking no argument in argparse

## Overview
`pylint file.py -v` failed with `argument --verbose/-v: expected one argument`, and `--help` advertised `--verbose VERBOSE, -v VERBOSE`. The long option only worked because `_preprocess_options` strips it before argparse sees it. Open PR #1001 preprocesses `-v` as well, which fixes the crash; this change fixes the underlying declaration so argparse itself knows the flag takes no value.

## Details
- `--verbose` and `--enable-all-extensions` use `_DoNothingAction` without `nargs`, so argparse expects one value (and prints a bogus metavar in help). They now pass `"kwargs": {"nargs": 0}` in `pylint/lint/base_options.py`.
- `_DoNothingAction` itself is deliberately left alone: `--rcfile`, `--output` and `--init-hook` also use it and do take a value.
- Builds on the `-v` preprocessing from #1001 (`PREPROCESSABLE_OPTIONS["-v"]`, `_preprocess_options` accepting single-dash options); that part is not duplicated here.
- Test: `tests/config/test_config.py::test_flag_options_take_no_argument` parses `[flag, "some_file.py"]` with the real argparse parser and checks the file name is not swallowed and the help has no `VERBOSE` / `ENABLE_ALL_EXTENSIONS` metavars.

## Verification
- Before: `pytest tests/config/test_config.py -k no_argument` -> 3 failed (`assert [] == ['some_file.py']`, the flag swallowed the file name).
- After: `pytest tests/config` -> 71 passed. `pylint --help` now shows `--verbose, -v` and `--enable-all-extensions` without metavars.
- `tests/test_self.py -k toml` fails on the base commit too (tomlkit "Can't add a table to a dotted key"), unrelated.
