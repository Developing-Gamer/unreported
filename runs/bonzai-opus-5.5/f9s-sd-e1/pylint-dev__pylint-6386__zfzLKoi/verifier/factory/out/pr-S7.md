Fix `-v` expecting an argument and `--verbose VERBOSE` in the help

## Overview
`pylint file.py -v` failed with `argument --verbose/-v: expected one argument` (exit 2), `pylint -v file.py` swallowed the file name as the option's value, and `--help` listed `--verbose VERBOSE, -v VERBOSE`. `-v` is now a plain flag, like `--verbose`, and the help no longer suggests a value.

## Details
- `pylint/config/utils.py`: the early option pre-processing only looked at arguments starting with `--` and had no `-v` entry, so `-v` was never handled. `-v` is added to `PREPROCESSABLE_OPTIONS` and arguments starting with a single `-` are now matched too.
- `pylint/lint/base_options.py`: `verbose` is registered with `nargs=0`, so argparse no longer expects a value for it and the help drops `VERBOSE`. (Not done on `_DoNothingAction` itself: `--rcfile`, `--output` and `--init-hook` use it and do take values.)
- `pylint/config/callback_actions.py`: docstring note on `nargs=0`.
- `ChangeLog` entry.
- Overlaps with #1001 on the `utils.py` pre-processing; #1001 does not touch the help/`nargs` part of the issue, which is covered here.

## Proof
- Before (base commit): `tests/config/test_config.py::test_short_verbose[first]` fails with `SystemExit: 32` (the file is not linted), `[last]` with `argparse.ArgumentError: argument --verbose/-v: expected one argument`, and `test_short_verbose_help` fails because the help has no `--verbose, -v`.
- After: all pass; `tests/config` 70 passed.

## Verification
`python -m pytest tests/config -q`
(`tests/test_self.py` cannot be collected in this environment: `ModuleNotFoundError: No module named 'py._path'`, unrelated to this change.)
