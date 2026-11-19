Fix `-v` being treated as an option that takes a value (SystemExit 2)

## Overview
`pylint file.py -v` exited with `argument --verbose/-v: expected one argument` (SystemExit 2), and `pylint -v file.py` swallowed the file name as the option's value so nothing was linted. `-v` now behaves as the flag it is documented to be and turns on verbose mode, like `--verbose`.

## Details
- Cause: the early option pre-processing step (`_preprocess_options`) only looked at arguments starting with `--` and `PREPROCESSABLE_OPTIONS` only listed `--verbose`. `-v` therefore reached argparse, where `verbose` is registered with a do-nothing action and no `nargs`, so argparse expects one value.
- Fix (`pylint/config/utils.py`): add `-v` to `PREPROCESSABLE_OPTIONS` and let `_preprocess_options` consider any argument starting with `-`. `-v` is consumed by pre-processing exactly as `--verbose` is.
- Test: `test_short_verbose_flag` in `tests/config/test_find_default_config_files.py` runs `Run(["-v", file])` and `Run([file, "-v"])`. Before the fix: `argparse.ArgumentError: argument --verbose/-v: expected one argument` -> `SystemExit: 2` (for -v last). After: both lint and print "No config file found, using default configuration".

## Verification
- `python -m pytest tests/config/test_find_default_config_files.py -k short_verbose` fails before, passes after.
- `tests/config` (67) and `tests/lint` (54, excluding `test_pylinter.py` which can't be collected here: `py._path` import error, unrelated) pass.
- `tests/test_self.py` cannot be collected in this sandbox (same unrelated import error).
