Fix `-v` short verbose flag failing with argparse "expected one argument" (SystemExit 2)

## Overview
`pylint file.py -v` (or `-v` alone) exited with `pylint: error: argument --verbose/-v: expected one argument` (SystemExit 2), and `pylint -v file.py` swallowed the file name as the flag's value. Sentry: 341 events / 58 users in 7 days.

## Cause
`--verbose` is registered with a `_DoNothingAction` and is handled in `_preprocess_options`, which strips it before argparse runs. Preprocessing only recognised the long `--verbose` (and only looked at arguments starting with `--`), so `-v` reached argparse, where `_DoNothingAction` has no `nargs=0` and therefore wants a value.

## Fix
Register `-v` in `PREPROCESSABLE_OPTIONS` and let `_preprocess_options` consider single-dash arguments, so `-v` is handled and removed exactly like `--verbose`. I did not force `nargs=0` on `_DoNothingAction`: it is shared with `--rcfile`, `--output` and `--init-hook`, which do take values.

## Verification
- New test `tests/test_self.py::TestCallbackOptions::test_verbose_short_flag` (`-v` before and after the module): fails before with `argument --verbose/-v: expected one argument`, passes after.
- `tests/test_self.py` and `tests/config`: the same 11 failures occur on the base commit (e.g. `test_pkginfo`, `test_generate_toml_config`, `toml_with_missing_comma`); no new failures.
- `python -m pylint tests/regrtest_data/empty.py -v` runs normally.
