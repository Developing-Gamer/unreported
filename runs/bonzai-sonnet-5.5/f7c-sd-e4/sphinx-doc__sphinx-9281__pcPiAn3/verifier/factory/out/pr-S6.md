Fix LaTeX abbreviation spacing when a period is followed by a newline or tab

## Problem
In PDF output, line-wrapped abbreviations (e.g. `e.g.` at the end of a line) had a wider gap before the next word, while HTML looked fine.

## Cause
`sphinx.util.texescape.escape_abbr` only added `\@{}` when a period was followed by a literal space or end of string (`(?= |$)`). A period followed by a newline or tab was left alone, so TeX treated it as a sentence end. The sibling helper in `sphinx/writers/latex.py` already uses `\s`.

## Fix
Use `r'\.(?=\s|$)'` in `texescape.escape_abbr`. Added `tests/test_util_texescape.py` (space, newline, tab, end of string, no-space cases) and a CHANGES entry.

## Verification
- Before: `tests/test_util_texescape.py` -> 2 failed (newline, tab), 3 passed.
- After: `tests/test_util_texescape.py tests/test_build_latex.py` -> 77 passed, 8 skipped.
- Run with `/opt/miniconda3/envs/testbed/bin/python -m pytest` (the default python 3.11 cannot import this Sphinx version).

The writer's own `escape_abbr` emits `\@` (not `\@{}`) and was left alone, since unifying would change output.
