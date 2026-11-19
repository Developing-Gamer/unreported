Fix whitespace in CREATE INDEX column lists (descending and opclass columns)

## Problem
`Index(fields=['-name'], name='idx')` generated `CREATE INDEX "idx" ON "schema_author" ("name"DESC)`: valid SQL but missing a space. The earlier opclasses fix also left a trailing space for ascending columns with an opclass (`"name" text_pattern_ops `).

## Fix
In `django/db/backends/ddl_references.py`:
- `Columns.__str__` now joins the quoted column and a non-empty suffix with a space (`"name" DESC`).
- `IndexColumns.__str__` appends the suffix only when it is non-empty, so no trailing space.

## Tests
New `ColumnSuffixesTests` in `tests/backends/test_ddl_references.py`. The `Columns` DESC test fails before the fix (`'"name"DESC' != '"name" DESC'`) and passes after.
Ran `python tests/runtests.py backends.test_ddl_references indexes schema model_indexes`: OK (PostgreSQL-only tests skipped on SQLite).
