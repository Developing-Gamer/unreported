gettext: keep every location of a message in the catalog

Root cause: `Catalog.add()` in `sphinx/builders/gettext.py` appended `(source, line, uid)` to `metadata[msg]` inside the `if msg not in self.metadata:` block. A phrase used on several pages therefore recorded only its first location, so the .pot file had a single `#:` source link.

Change: dedent the append so every origin is recorded, and the first one still initialises the list. Added a CHANGES entry.

Verification: added `test_catalog_keeps_all_locations_of_a_message` in tests/test_build_gettext.py (fails before, passes after). tests/test_build_gettext.py passes. tests/test_intl.py has 5 failures that also fail without this change.
