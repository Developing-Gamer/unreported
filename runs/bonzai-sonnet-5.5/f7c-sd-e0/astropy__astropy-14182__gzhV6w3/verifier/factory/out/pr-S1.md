Support header_rows in the ascii.rst (RestructuredText) writer and reader

## Overview
`tbl.write(sys.stdout, format="ascii.rst", header_rows=["name", "unit"])` raised `TypeError: __init__() got an unexpected keyword argument 'header_rows'`, although `ascii.fixed_width` supports the option. The RST format now accepts `header_rows` for both writing and reading.

## Details
- `RST.__init__` accepts `header_rows` and passes it to `FixedWidth`.
- `RST.write` used `lines[1]` as the border line; it now uses `lines[len(header_rows)]`, the position line, so the top and bottom borders are correct with multiple header rows.
- The data start line was fixed at 3; it is now `len(header_rows) + 2`, so reading with `header_rows` finds the data.
- Default (single `name` row) output is unchanged. Docstring and a changelog entry added.

## Before / After
Before: `TypeError: __init__() got an unexpected keyword argument 'header_rows'`.
After:
```
===== ========
 wave response
   nm       ct
===== ========
350.0      0.7
950.0      1.2
===== ========
```

## Verification
- New test `test_rst_with_header_rows` (write plus read round trip) failed with the TypeError before the fix and passes after.
- `pytest astropy/io/ascii/tests`: 825 passed, 36 skipped, 6 xfailed.
- The changelog filename uses 13734 as the PR number; adjust it to the real number.
