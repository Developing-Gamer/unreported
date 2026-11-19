Fix `-v` (short verbose flag) failing with "expected one argument" (SystemExit 2)

## Problem
`pylint file.py -v` exits with `argument --verbose/-v: expected one argument` (SystemExit 2), and `pylint -v file.py` swallows the file name as the value of `-v` (exit 32). 341 Sentry events in 7 days.

## Cause
`--verbose` is handled in `_preprocess_options` and removed from the argument list before argparse sees it. The preprocessor only looked at arguments starting with `--` and `PREPROCESSABLE_OPTIONS` only listed `--verbose`, so `-v` reached argparse, where its `_DoNothingAction` makes it expect a value.

## Fix
- Register `-v` in `PREPROCESSABLE_OPTIONS` with the same callback as `--verbose`.
- Let `_preprocess_options` consider any argument starting with `-` (not just `--`).

`_DoNothingAction` was left unchanged: forcing `nargs=0` on it would also change the other options that use it and take a value (`--rcfile`, `--output`, `--init-hook`), and is not needed once `-v` is preprocessed.

## Verification
- New `tests/config/test_config.py::test_short_verbose` (`-v` after the file, before the file, and `--verbose`): fails before the fix with `SystemExit: 2` / `SystemExit: 32`, passes after.
- `pytest tests/config tests/test_self.py tests/lint`: 239 passed; 2 failures (`test_generate_toml_config*`) fail identically on the base commit.
