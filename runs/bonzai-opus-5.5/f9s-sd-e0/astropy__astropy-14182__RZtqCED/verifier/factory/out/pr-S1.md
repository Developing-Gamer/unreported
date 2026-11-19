Support header_rows in the ascii.rst (RestructuredText) format

## Overview
`tbl.write(..., format="ascii.rst", header_rows=["name", "unit"])` raised `TypeError: __init__() got an unexpected keyword argument 'header_rows'`, although `ascii.fixed_width` supports it. The RST writer/reader now accepts `header_rows` and handles any number of header rows.

## Details
- `RST.__init__` accepts `header_rows` and forwards it to `FixedWidth`.
- `RST.write` took the `=====` border from the hard-coded `lines[1]`; it now uses `lines[len(header_rows)]`.
- For reading, the data start line was fixed at 3; it is now `len(header_rows) + 2`.
- Default behaviour (`header_rows=None` -> `["name"]`) is unchanged.
- Tests: write with `["name", "unit"]` and a round trip restoring units (both fail with the TypeError before the change). Changelog fragment added (docs/changes/io.ascii/14000.feature.rst; rename to the real PR number).

## Verification
`pytest astropy/io/ascii/tests/test_rst.py astropy/io/ascii/tests/test_fixedwidth.py` — 46 passed.
