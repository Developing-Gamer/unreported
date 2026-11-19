Use proper whitespace in CREATE INDEX column lists

## Root cause
`Index.create_sql()` passes one column suffix per field: `'DESC'` for descending fields and `''` for ascending ones. In `django/db/backends/ddl_references.py`:

- `Columns.__str__()` joined the quoted column and the suffix with nothing between them, so a descending index came out as `("name"DESC)`.
- `IndexColumns.__str__()` (PostgreSQL opclasses) always added `' ' + suffix`. The fix for #30903 assumed ascending columns would have no suffix at all, but they get an empty string, so `("name" text_pattern_ops )` came out with a trailing space.

## Change
In both `Columns.__str__()` and `IndexColumns.__str__()`, the suffix is added (with one space before it) only when it is non-empty. The output is now:

- `("name")` and `("name" DESC)`
- `("name" text_pattern_ops)` and `("name" text_pattern_ops DESC)`

## Verification
- New unit tests in `tests/backends/test_ddl_references.py` (`ColumnsSuffixesTests`, `IndexColumnsTests`) that check `Columns`/`IndexColumns` rendering with empty and `DESC` suffixes, with and without opclasses.
- New tests in `tests/indexes/tests.py`: `test_columns_list_sql` and `test_descending_columns_list_sql` run on all backends; `test_ops_class_columns_lists_sql` and `test_ops_class_descending_columns_list_sql` run on PostgreSQL only.
- Without the fix, the new tests fail (`"FIRST_COLUMN"DESC`, a trailing space after the opclass, `"headline"DESC`). With the fix, `runtests.py backends.test_ddl_references indexes schema model_indexes migrations.test_operations admin_filters backends` passes on SQLite. The PostgreSQL-only tests were skipped here because no PostgreSQL database was available.
