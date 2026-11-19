Fix Node.add_marker(append=False) inserting at index 1 instead of 0

## Overview
Plugins that call `item.add_marker(mark, append=False)` expect their mark to come first, as documented. It was inserted at index 1, so on a test that already had a `skip` mark the plugin's mark landed after it, and the original skip reason was reported instead of the plugin's. On tests with no marks index 1 acts like an append, which is why those looked correct.

## Details
- `src/_pytest/nodes.py`: `own_markers.insert(1, ...)` -> `insert(0, ...)`, matching the docstring.
- `testing/test_skipping.py`: new test where a test has `@pytest.mark.skip(reason="a")` and a conftest adds `skip(reason="b")` with `append=False`; the report must say `b`. It fails before the fix (reports `a`).
- `testing/test_mark.py::test_addmarker_order` already asserted the correct order.
- Changelog `6211.bugfix.rst`. (The number is a placeholder; rename to the real issue/PR number.)

## Verification
`pytest testing/test_skipping.py testing/test_mark.py` passes.
