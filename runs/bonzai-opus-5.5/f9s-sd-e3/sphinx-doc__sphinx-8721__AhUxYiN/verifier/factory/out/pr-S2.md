Fix gettext Catalog dropping source locations of repeated messages

## Overview
A phrase used on several documentation pages produced a `.pot` entry with only one `#:` source reference (and one uuid). `Catalog.add` appended the origin only when the msgid was first seen, so every later occurrence in other documents was discarded.

## Details
- `sphinx/builders/gettext.py`: dedent the `self.metadata[msg].append(...)` line so it runs on every `add`, while the msgid is still registered only once.
- `tests/test_build_gettext.py`: regression test `test_catalog_keeps_all_locations_of_repeated_message` adds the same msg from two files and asserts both locations and two distinct uuids.

## Verification
- New test fails before the fix, passes after.
- `tests/test_build_gettext.py` passes. `tests/test_intl.py` has 3 failures (test_html_meta, test_additional_targets_*) that fail identically on the base commit.
