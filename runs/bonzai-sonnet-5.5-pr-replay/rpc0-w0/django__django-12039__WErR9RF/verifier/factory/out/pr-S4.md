Use proper whitespace in CREATE INDEX statements

## Overview
`Index(fields=['-name'], name='idx')` generated `CREATE INDEX "idx" ON "schema_author" ("name"DESC)`, and on PostgreSQL an index with `opclasses` but no explicit ordering generated `("name" text_pattern_ops )` with a stray trailing space. Both are valid SQL but ugly. Columns are now rendered as `"name" DESC` and `"name" text_pattern_ops`.

## Details
- `Columns.__str__` now joins the quoted column and a non-empty suffix with a space.
- `IndexColumns.__str__` only appends the suffix (with a leading space) when it is non-empty.
- Added unit tests in `tests/backends/test_ddl_references.py`: DESC without opclasses, opclasses without ordering, opclasses with DESC. Before the fix they fail with `'FIRST_COLUMN, SECOND_COLUMNDESC' != 'FIRST_COLUMN, SECOND_COLUMN DESC'` and `'FIRST_COLUMN a , SECOND_COLUMN b ' != ...`.

## Verification
`PYTHONPATH=/testbed python tests/runtests.py backends.test_ddl_references schema indexes model_indexes --parallel 1` — 199 tests OK (33 skipped, PostgreSQL-only).
