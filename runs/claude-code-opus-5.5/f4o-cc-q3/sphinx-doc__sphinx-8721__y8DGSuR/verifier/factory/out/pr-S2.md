gettext: record every location of a repeated message in the catalog

## Root cause
In `sphinx/builders/gettext.py`, `Catalog.add()` had the `self.metadata[msg].append(...)` call indented inside the `if msg not in self.metadata:` block. Only the first occurrence of a msgid stored its origin (source, line, uid). Later occurrences were dropped, so the generated `.pot` listed a single `#:` location for a phrase used on several pages. Translation tools then showed only one source link for it.

## Change
Moved the `append` out of the `if` block. A new msgid is still registered once (which keeps insertion order), and every occurrence now records its origin.

## Verification
- New test `tests/test_build_gettext.py::test_catalog_keeps_all_locations_of_duplicate_message` adds the same msgid from two origins and checks that both locations and uuids are kept. It fails before the change and passes after.
- `pytest tests/test_build_gettext.py`: all tests pass.
