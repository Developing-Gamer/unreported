Fix `Node.add_marker(append=False)` inserting at index 1 instead of 0

## Root cause
`Node.add_marker()` in `src/_pytest/nodes.py` is documented to insert the marker at position 0 when `append=False`, but it called `self.own_markers.insert(1, ...)`. If a node has no own markers, inserting at index 1 still puts the marker first, so that case looked correct. If the test already has a marker (e.g. `@pytest.mark.skip(reason="default ...")`), the prepended marker ends up *after* it. The skipping plugin uses the first `skip` marker from `iter_markers()`, so the original/default reason wins over the one the plugin supplied. This matches the report: only tests that already had a skip annotation show the wrong reason.

## Change
- `own_markers.insert(1, ...)` → `own_markers.insert(0, ...)`.

## Verification
- The existing `testing/test_mark.py::test_addmarker_order` (expects `["baz", "foo", "bar"]`) failed before the change and passes now.
- New `testing/test_skipping.py::test_skip_marker_prepended_by_plugin_takes_precedence`: a conftest prepends `skip(reason="plugin reason")` to a test that already has `skip(reason="default reason")`. With `-rs` the output shows the plugin reason. The test fails before the change and passes after it.
- Ran `testing/test_mark.py`, `test_skipping.py`, `test_collection.py`, `test_terminal.py`: all pass.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
