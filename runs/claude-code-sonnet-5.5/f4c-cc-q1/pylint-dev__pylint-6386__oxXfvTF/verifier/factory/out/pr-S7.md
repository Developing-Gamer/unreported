Fix `pylint -v` failing with "expected one argument"

## Root cause
`--verbose` is handled by `_preprocess_options` before argparse runs, so argparse never sees it. The short form `-v` was not in `PREPROCESSABLE_OPTIONS`, and the preprocessor only looked at arguments starting with `--`. `-v` therefore reached argparse. There, `verbose` is registered with `_DoNothingAction` without `nargs=0`, so it demanded a value and exited with `pylint: error: argument --verbose/-v: expected one argument`. That is the `SystemExit: 2` in S4. The help text also wrongly showed `--verbose VERBOSE`.

## Change
- `pylint/config/utils.py`: add `-v` to `PREPROCESSABLE_OPTIONS` and let the preprocessor inspect any argument starting with `-`. `-v` now sets `run.verbose` like `--verbose`.
- `pylint/lint/base_options.py`: set `nargs=0` for `verbose` and `enable-all-extensions`, so argparse (and `--help`) treat them as flags. `enable-all-extensions` had the same defect in its help output.
- `tests/test_self.py`: add `test_short_verbose`, which checks that `-v` and `--verbose` both run and set `run.verbose`.

Also covers S4, the production Sentry event for the same failure.

## Verification
- `test_short_verbose` fails without the fix (SystemExit) and passes with it.
- `pylint file.py -v` now runs normally. `--help` shows `--verbose, -v` with no value.
- `tests/test_self.py` and `tests/config` have the same 11 failures before and after the change, so none are caused by it. I did not investigate them.
