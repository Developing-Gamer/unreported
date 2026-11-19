Fix `-v` short verbose flag exiting with "expected one argument"

## Overview
`pylint file.py -v` exited with `argument --verbose/-v: expected one argument` (SystemExit 2), and `pylint -v file.py` swallowed the file name as the option's value and linted nothing. Sentry shows 341 such events (58 users) in 7 days. `-v` now behaves exactly like `--verbose`.

## Details
- Root cause: the `verbose` option is registered with a do-nothing action and no `nargs`, so argparse wants one value. `--verbose` never reached argparse because the early option preprocessing consumes it; `-v` was skipped there (only `--` arguments were considered, and only `--verbose` was listed).
- `pylint/config/utils.py`: add `-v` to `PREPROCESSABLE_OPTIONS`; `_preprocess_options` now looks at any argument starting with `-` (unknown ones are passed through unchanged).
- `pylint/lint/base_options.py`: give the verbose option `nargs=0`, so argparse treats it as a flag.
- Test: `test_short_verbose_output_no_config` in `tests/config/test_find_default_config_files.py` covers `-v file`, `file -v` and `-v` alone.

## Verification
- New test fails before the fix with `expected one argument` (3 cases), passes after.
- `tests/config tests/lint tests/test_self.py`: same 11 pre-existing failures (tomlkit / test_self environment issues) with and without the change; no new failures.
