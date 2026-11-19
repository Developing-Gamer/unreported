Reject malformed font patterns instead of treating them as unknown font families

`parse_fontconfig_pattern` returned `{"family": [pattern]}` for any unparseable pattern without a colon. Strings such as `Helvetica-Bold` or `serif-12pt` (e.g. in a saved style's `mathtext.rm`, or `FontProperties("serif-12pt")`) were accepted as a nonexistent family, so export silently fell back to the default font/size rather than reporting an invalid font setting.

This removes that catch-all so every `ParseException` becomes a `ValueError`, as it was for patterns containing a colon. Valid names such as `serif` or `DejaVu Sans` still parse via the family grammar.

Test: `test_fontconfig_invalid_pattern` in `lib/matplotlib/tests/test_fontconfig_pattern.py` (fails before with "DID NOT RAISE ValueError", passes after).

Verification: test_fontconfig_pattern, test_mathtext, test_font_manager, test_text and test_rcparams pass, except `test_rcparams_update` / `test_rcparams_init`, which also fail on the base commit (unrelated: they expect a "validate" warning that isn't emitted).
