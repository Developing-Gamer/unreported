Fix malformed fontconfig patterns being silently accepted as family names

`parse_fontconfig_pattern` swallowed a `ParseException` for any pattern without a `:` and returned `{"family": [pattern]}`. A malformed pattern such as `Sans-abc` or `DejaVu Sans-12-` was therefore accepted as a made-up family name: its size/weight/style were dropped, `validate_font_properties` (used for the `mathtext.*` rcParams) did not report it, and the font silently fell back to the default font at size 10.

The fallback is removed, so every parse failure raises `ValueError` with the parser's explanation again.

Tests: added `test_fontconfig_invalid_pattern` (fails before the fix with "DID NOT RAISE", passes after). `test_fontconfig_pattern.py`, `test_font_manager.py`, `test_mathtext.py` pass. `test_rcparams_update`/`test_rcparams_init` fail identically on the base commit (unrelated, missing UserWarning).
