Use proper whitespace in CREATE INDEX statements

`Columns.__str__` concatenated the quoted column and its `DESC` suffix with no separator, producing `("name"DESC)`. `IndexColumns.__str__` (PostgreSQL, used with opclasses) always appended a space plus the suffix, so a column with no explicit ordering rendered as `("name" text_pattern_ops )` with a stray trailing space.

Both now add a single space before the suffix only when the suffix is non-empty, giving `("name" DESC)` and `("name" text_pattern_ops)`.

Tests: added unit tests in `tests/backends/test_ddl_references.py` for `Columns` with `DESC`, and `IndexColumns` with opclasses and an empty suffix. Before the fix they fail (e.g. `'FIRST_COLUMN a , SECOND_COLUMN b DESC' != 'FIRST_COLUMN a, SECOND_COLUMN b DESC'`).

Verification: `cd tests && PYTHONPATH=/testbed python runtests.py backends.test_ddl_references schema indexes` passes (183 tests, PostgreSQL-only ones skipped on SQLite).
