LaTeX: apply abbreviation spacing fix to periods followed by any whitespace

Root cause: `sphinx.util.texescape.escape_abbr()` used the lookahead `(?= |$)`,
so only a period followed by a literal space (or end of string) received the
`\@` marker. A period followed by a newline/tab (e.g. line-wrapped source text)
was not matched, so LaTeX treated it as a sentence end and inserted a wider gap
before the next word in the PDF, while HTML looked unchanged (source S6). The
sibling `escape_abbr` in `sphinx/writers/latex.py` already used `\s`.

Change: the lookahead is now `(?=\s|$)`. Added `tests/test_util_texescape.py` and a
CHANGES entry.

Verification: `pytest tests/test_util_texescape.py tests/test_util_inspect.py
tests/test_build_latex.py` -> 112 passed, 8 skipped.
