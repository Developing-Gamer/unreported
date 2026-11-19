Keep fractional glyph widths when parsing AFM metrics

## Overview
Fonts whose AFM files give fractional glyph widths (e.g. `WX 611.9`) had each width truncated to an integer when parsed. The PDF/PS backends sum these widths to measure a label for alignment, so long labels were measured too narrow; right-aligned text then ended past its anchor, by more the longer the label. The 14 standard fonts have whole-number widths, so they were unaffected.

## Details
- `lib/matplotlib/_afm.py`: `_parse_char_metrics` parsed `WX` with `_to_int`; it now uses `_to_float`.
- `lib/matplotlib/tests/test_afm.py`: new `test_fractional_char_widths` checks a `WX 611.9` glyph reports 611.9 and a 40-glyph string reports 40 * 611.9. It failed before the fix (`Obtained: 611`).

## Verification
- `python -m pytest lib/matplotlib/tests/test_afm.py` fails before the fix, passes after.
- `python -m pytest lib/matplotlib/tests/test_afm.py lib/matplotlib/tests/test_backend_ps.py lib/matplotlib/tests/test_backend_pdf.py`: 61 passed.
