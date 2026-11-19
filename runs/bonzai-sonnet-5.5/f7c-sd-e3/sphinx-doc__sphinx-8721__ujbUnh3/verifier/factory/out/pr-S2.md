Fix gettext builder recording only the first location of a repeated message

## Overview
A phrase used on several documents showed only one `#:` source location (and one uuid) in the generated `.pot`, so translators saw a single source link. `Catalog.add` only appended `(source, line, uid)` the first time a message was seen. It now records every occurrence.

## Details
- `sphinx/builders/gettext.py`: dedent the `self.metadata[msg].append(...)` line in `Catalog.add` out of the `if msg not in self.metadata` branch; list initialisation stays inside.
- New test `test_gettext_all_locations_of_repeated_message` (root `test-gettext-locations`): two documents with the same paragraph, built into one catalog; asserts a `#:` line for each.

## Verification
- `python -m pytest tests/test_build_gettext.py -k repeated`: fails before (`assert '#: ../../other.rst:' in '#: ../../index.rst:8\n'`), passes after.
- `tests/test_build_gettext.py` passes; `tests/test_intl.py` has 5 failures (test_gettext_toctree, test_html_meta, test_xml_label_targets, test_additional_targets_*) that fail identically on the base commit.
