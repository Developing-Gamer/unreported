Fix short `-v` verbose option requiring an argument (fixes S7, S4)

## Root cause

`--verbose` and `--enable-all-extensions` are handled in `_preprocess_options`
(`pylint/config/utils.py`) before argparse runs, and are registered with argparse only
through `_DoNothingAction`, so that later parsing doesn't reject them. Two problems:

1. The preprocessor only looked at arguments starting with `--`, and
   `PREPROCESSABLE_OPTIONS` had no `-v` entry. So `-v` went straight to argparse.
2. `_DoNothingAction` is a plain `argparse.Action` with the default `nargs=None`, so
   argparse expected one value for it. As a result `pylint mod.py -v` exited with
   `pylint: error: argument --verbose/-v: expected one argument` (`SystemExit: 2`), and
   `--help` showed `--verbose VERBOSE, -v VERBOSE` and
   `--enable-all-extensions ENABLE_ALL_EXTENSIONS`.

The production Sentry event S4 (`SystemExit: 2` raised from argparse's
`consume_optional` → `error`, via `_parse_command_line_configuration`) is this same
failure.

## Change

- `pylint/config/utils.py`: register `-v` as a preprocessable option (it calls the same
  `_set_verbose_mode` as `--verbose`), and let the preprocessor look at any argument
  starting with `-`, not just `--`. Only options listed in `PREPROCESSABLE_OPTIONS` are
  consumed; every other short option still goes through unchanged.
- `pylint/lint/base_options.py`: pass `nargs=0` to argparse for `verbose` and
  `enable-all-extensions`. Argparse then treats them as flags, and the help no longer
  suggests they take a value.
- `ChangeLog` entry.

## Verification

- New tests in `tests/config/test_config.py`:
  - `test_short_and_long_verbose_flags[-v|--verbose]`: `Run([...,"-v"])` sets
    `run.verbose` and doesn't error.
  - `test_verbose_help_has_no_metavar`: `--help` shows `--verbose, -v` and no `VERBOSE`.
  - Without the library change, the `-v` test and the help test fail; with it, all pass.
- Manually: `pylint mod.py -v` now lints and prints `Using config file ...`, i.e.
  verbose mode is on.
- Ran `tests/config`, `tests/test_self.py` and `tests/lint`: 11 tests fail with and
  without this change, and the failing lists are identical. They are environment-related
  failures that already existed (e.g. `test_bom_marker` sees unrelated
  `useless-suppression` output). The change introduces no new failures.
