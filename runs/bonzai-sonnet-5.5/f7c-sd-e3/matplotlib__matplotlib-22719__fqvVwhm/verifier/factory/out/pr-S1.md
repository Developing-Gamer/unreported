Fix PDF/PS text width measurement for TrueType fonts so right-aligned long labels don't overshoot

## Overview
For TrueType fonts, `RendererPDFPSBase.get_text_width_height_descent` measured text with `FT2Font.set_text` (grid-fitted kerning, truncated integer glyph advances), while `RendererPdf.draw_text` places glyphs using `_text_helpers.layout` with `KERNING_UNFITTED` and unhinted `linearHoriAdvance`. The two widths diverge with string length, so long right-aligned (or centered) labels were positioned using the wrong width and ended past their anchor. AFM standard fonts measure and draw from the same data and were unaffected.

## Details
- Add `_text_helpers.layout_width`, the end position of `layout()` (last glyph x + linearHoriAdvance).
- `get_text_width_height_descent` uses it for the width in the TTF branch (height/descent still from `set_text`).
- Add a `_kern_mode` class attribute on `RendererPDFPSBase` (default `KERNING_DEFAULT`, what PS draws with); `RendererPdf` sets `KERNING_UNFITTED` and uses it in `draw_text`, so measuring and drawing share one setting.
- Regenerated PDF baselines `test_text/multiline.pdf` and `test_text/text_alignment.pdf` (sub-pixel alignment shifts from the corrected widths).

## Verification
- New test `test_backend_pdf.py::test_text_width_matches_layout` (pdf/ps x DejaVu Sans/cmr10): failed before (e.g. 1870.94 vs 1871.39), passes now.
- test_text, test_backend_pdf, test_backend_ps, test_mathtext, test_usetex: 1234 passed, 511 skipped.
