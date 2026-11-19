Support header_rows in the ascii.rst reader and writer

## Overview
`tbl.write(sys.stdout, format="ascii.rst", header_rows=["name", "unit"])` raised `TypeError: __init__() got an unexpected keyword argument 'header_rows'`, although `ascii.fixed_width` supports the option. `ascii.rst` now accepts `header_rows` for both writing and reading.

## Details
- `RST.__init__` takes `header_rows` and passes it to `FixedWidth`.
- The data start line was hardcoded to 3; it is now `len(header_rows) + 2` (opening border, header rows, position line).
- `RST.write` took the `=` border from `lines[1]`; it now uses `lines[len(header_rows)]`, so the borders are right with any number of header rows. The default output is unchanged.
- Docstring and changelog entry (`docs/changes/io.ascii/14182.feature.rst`; the number is a guess and should be replaced with the real PR number).

## Verification
- New test `test_rst_with_header_rows` (write, then read back names, units and values) failed before the fix with the TypeError above and passes now.
- `pytest astropy/io/ascii/tests/`: 825 passed, 36 skipped, 6 xfailed.
- No visual change; nothing on screen to capture.
