Fix `Node.add_marker(append=False)` inserting at the wrong position

Root cause: `Node.add_marker` documents that with `append=False` the marker is inserted at position 0, but the code used `own_markers.insert(1, ...)`. When the node already had a marker (e.g. an existing `@pytest.mark.skip(reason=...)`), the plugin's new marker landed second, and because `pytest_runtest_setup` uses the first skip marker found, the original reason was reported instead of the plugin's. Nodes with no existing markers happened to work since inserting at index 1 of an empty list appends.

Change: insert at index 0 in `src/_pytest/nodes.py`.

Verification: added `test_add_marker_skip_prepended_overrides_existing_skip` in testing/test_skipping.py; the existing `test_addmarker_order` in testing/test_mark.py (which failed before) passes now. Added changelog/6241.bugfix.rst.
