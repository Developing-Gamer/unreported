Use proper whitespace in CREATE INDEX statements

## Overview
`Index(fields=['-name'])` generated `CREATE INDEX "idx" ON "t" ("name"DESC)`, and on PostgreSQL an index with `opclasses` but ascending order generated `("name" text_pattern_ops )` with a trailing space. Both are valid SQL but malformed-looking. The column list is now rendered with a single space between the column (or opclass) and the suffix, and no space when the suffix is empty.

## Details
- `Columns.__str__` joined the quoted column straight to the suffix; it now adds `' ' + suffix` only when the suffix is non-empty.
- `IndexColumns.__str__` always appended `' ' + suffix`, leaving a trailing space for ascending columns; it now appends only a non-empty suffix.
- Tests added in `tests/backends/test_ddl_references.py` for DESC, empty suffix, opclass with empty suffix, opclass with DESC, and opclass without suffixes.

## Verification
- `cd tests && PYTHONPATH=/testbed python runtests.py backends.test_ddl_references` fails before the fix and passes after.
- `backends.test_ddl_references indexes schema model_indexes`: 205 tests OK (SQLite; PostgreSQL-only tests skipped).
