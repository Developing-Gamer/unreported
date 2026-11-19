Support `header_rows` in the `ascii.rst` format (also fixes S4 `-OO` import crash)

## Root cause
`RST.__init__` took no arguments, so `header_rows` (supported by `FixedWidth`) raised `TypeError`. The RST data start line (3) and the closing-border index (`lines[1]`) were hard-coded for a single header row.

## Change
- `RST.__init__(header_rows=None)` forwards to `FixedWidth`; the data start line is `len(header_rows) + 2`, and `write` uses the border line after the last header row.
- S4 (shares this PR): `MetaBaseReader` now uses `inspect.cleandoc(cls.__doc__ or "")`, so `import astropy.io.ascii` no longer crashes when docstrings are absent (`python -OO`).
- Changelog entries added.

## Verification
- New tests: `test_rst_with_header_rows` (read and write round trip with name/unit/dtype) and `test_reader_class_without_docstring`. Both fail before the change and pass after.
- Confirmed `python -OO -c "import astropy.io.ascii"` failed before and works now.
- `pytest astropy/io/ascii` passes; the remaining failures are pre-existing BLS/network-related ones in `astropy/timeseries`.
