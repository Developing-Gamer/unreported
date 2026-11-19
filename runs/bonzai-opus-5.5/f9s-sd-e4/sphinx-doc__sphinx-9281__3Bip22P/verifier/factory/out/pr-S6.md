latex: add abbreviation spacing after a period followed by any whitespace

## Overview
In PDF output, abbreviations that end a line (e.g. in the project/author title page fields or Fig./Table. caption names) could be followed by a wider inter-sentence gap. `sphinx.util.texescape.escape_abbr` only inserted `\@{}` when the period was followed by a literal space or end of string, so a period before a newline or tab was treated by LaTeX as a sentence end. HTML is unaffected.

## Details
- `escape_abbr` lookahead changed from `(?= |$)` to `(?=\s|$)` (same as the LaTeX writer's own helper and upstream).
- New `tests/test_util_texescape.py` covers space, end of string, newline, tab and a non-abbreviation (`3.14`).
- CHANGES entry added.

## Verification
- `python -m pytest tests/test_util_texescape.py` failed before the fix (`e.g.\nnext` not escaped), passes after.
- `python -m pytest tests/test_util_texescape.py tests/test_build_latex.py`: 73 passed, 8 skipped.
